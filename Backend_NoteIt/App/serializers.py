from rest_framework import serializers
from .models import User,Note,Category
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    def to_representation(self, instance):
        token = RefreshToken.for_user(instance)
        return {
            'message': 'User registered successfully.',
            'user': {
                'email': instance.email,
                'username': instance.username
            },
            'token': {
                'refresh': str(token),
                'access': str(token.access_token),
            }
        }


class NoteSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=False)
    category = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'description', 'is_file', 'file_url', 'file', 'category', 'created_at', 'updated_at']
        read_only_fields = ['user', 'file_url', 'created_at', 'updated_at']

    def validate_file(self, value):
        if value and not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        return value

    def create(self, validated_data):
        file = validated_data.pop('file', None)
        category_name = validated_data.pop('category', None)
        user = self.context['request'].user
        validated_data.pop('user', None)

        category = None
        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)

        note = Note.objects.create(user=user, category=category, **validated_data)

        if file:
            import cloudinary.uploader
            upload_result = cloudinary.uploader.upload(file, resource_type='raw')
            note.file_url = upload_result['secure_url']
            note.is_file = True
            note.save()

        return note

    def update(self, instance, validated_data):
        file = validated_data.pop('file', None)
        category_name = validated_data.pop('category', None)

        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)
            instance.category = category
        else:
            instance.category = None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if file:
            import cloudinary.uploader
            upload_result = cloudinary.uploader.upload(file, resource_type='raw')
            instance.file_url = upload_result['secure_url']
            instance.is_file = True

        instance.save()
        return instance
