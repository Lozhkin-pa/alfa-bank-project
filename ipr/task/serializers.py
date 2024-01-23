from rest_framework import serializers

from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    # ipr = serializers.StringRelatedField(
    #     read_only=True
    # )

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'status',
            'author',
            # 'ipr',
            'deadline',
            'created_date'
        )


class CreateTaskSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

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
            instance.deadline = validated_data.get(
                'deadline',
                instance.deadline
            )
        # if request.user == instance.employee:
        #     instance.status = validated_data.get(
        #         'status',
        #         instance.status
        #     )
        instance.save()
        return instance

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'status',
            'author',
            # 'ipr',
            'deadline',
            'created_date'
        )
