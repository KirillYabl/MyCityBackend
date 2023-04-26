from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            err_msg = 'Users require an email field'
            raise ValueError(err_msg)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            err_msg = 'Superuser must have is_staff=True.'
            raise ValueError(err_msg)
        if extra_fields.get('is_superuser') is not True:
            err_msg = 'Superuser must have is_superuser=True.'
            raise ValueError(err_msg)

        return self._create_user(email, password, **extra_fields)
