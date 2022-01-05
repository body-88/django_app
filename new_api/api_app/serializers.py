from django.db.models import fields
from rest_framework import request, serializers
from rest_framework.fields import CurrentUserDefault
from api_app.models import User, UserProfile, DocumentRequest


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "city",
            "gender",
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ("url", "email", "first_name", "last_name", "password", "profile")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile")
        profile = instance.profile

        instance.email = validated_data.get("email", instance.email)
        instance.save()

        profile.city = profile_data.get("city", profile.city)
        profile.gender = profile_data.get("gender", profile.gender)

        profile.save()

        return instance


class DocumentRequestSerializer(serializers.ModelSerializer):
    # from_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    from_user = serializers.EmailField(read_only=True)
    # to_user = serializers.EmailField(read_only=True, source='to_user')
    
    class Meta:
        
        model = DocumentRequest
        fields = (
            "from_user",
            "to_user",
            "time",
            "status_request",
        )
        read_only_fields = (
            "status_request",
            
            
        )
    
    def validate(self, data):
        
        
        if data['to_user'] == self.context['request'].user:
            raise serializers.ValidationError('You cannot send request to yourself')
   
        return data
    


class DocumentReceivedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentRequest
        fields = ("from_user", "to_user", "time", "status_request", "file")
        read_only_fields = (
            "from_user",
            "status_request",
        )
