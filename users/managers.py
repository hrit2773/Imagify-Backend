from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        
        if not extra_fields.get('is_staff'):
            raise ValueError('not is_staff')
        
        if not extra_fields.get('is_superuser'):
            raise ValueError('not is_superuser')
        
        return self.create_user(
            email,
            password,
            **extra_fields
        )
        
    