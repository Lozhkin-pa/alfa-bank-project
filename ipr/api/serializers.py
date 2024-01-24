from rest_framework import serializers
from iprs.models import Ipr
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "photo",
            "username",
            "firstname",
            "lastname",
            "patronymic",
            "email",
            "position",
            "superior",
            "subordinates",
        ]


class ReadIprSerializer(serializers.ModelSerializer):
    # tasks = serializers.StringRelatedField(
    #     many=True,
    #     read_only=True
    # )
    author = serializers.StringRelatedField(
        read_only=True
    )
    employee = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Ipr
        fields = (
            'id',
            'title',
            'employee',
            'author',
            'description',
            'status',
            'created_date',
            'end_date',
            # 'tasks',
        )


class CreateIprSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField( 
        queryset=User.objects.all(),
    )

    def create(self, validated_data):
        if Ipr.objects.filter(
            title=validated_data.get('title'),
            employee=validated_data.get('employee')
        ).exists():
            raise serializers.ValidationError(
                {'errors': 'Такой ИПР уже существует!'}
            )
        request = self.context.get('request')
        # if validated_data.get('employee') == request.user.subordinates:
        if request.user.superior: # Если руководитель/подчиненный определяется в модели User типом bool
            ipr = Ipr.objects.create(**validated_data)
        return ipr

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request.user == instance.author:
            instance.title = validated_data.get(
                'title',
                instance.title
            )
            instance.description = validated_data.get(
                'description',
                instance.description
            )
            instance.status = validated_data.get(
                'status',
                instance.status
            )
            instance.end_date = validated_data.get(
                'end_date',
                instance.end_date
            )
        if request.user == instance.employee:
            instance.status = validated_data.get(
                'status',
                instance.status
            )
        instance.save()
        return instance

    def to_representation(self, obj):
        request = self.context.get('request')
        serializer = ReadIprSerializer(
            obj,
            context={'request': request}
        )
        return serializer.data

    class Meta:
        model = Ipr
        fields = (
            'title',
            'employee',
            'description',
            'status',
            'end_date',
        )
