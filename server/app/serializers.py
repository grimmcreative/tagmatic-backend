from marshmallow import Serializer, fields


class UserSerializer(Serializer):
    class Meta:
        fields = ("id", "email")


class PostSerializer(Serializer):
    user = fields.Nested(UserSerializer)

    class Meta:
        fields = ("id", "title", "body", "user", "created_at")


class ToDoSerializer(Serializer):
    class Meta:
        fields = ("id", "text", "is_complete", "created_at", "status")


class ContactSerializer(Serializer):
    class Meta:
        fields = ("id", "first_name", "last_name", "text", "created_at")

