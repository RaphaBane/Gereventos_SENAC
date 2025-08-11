from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import Evento
import cloudinary.uploader


@receiver(pre_delete, sender=Evento)
def deletar_banner_cloudinary(sender, instance, **kwargs):
    if instance.imagem_banner:
        cloudinary.uploader.destroy(instance.imagem_banner.public_id)

@receiver(pre_save, sender=Evento)
def deletar_banner_antigo_ao_atualizar(sender, instance, **kwargs):
    if instance.pk:
        try:
            antigo_evento = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return

        if antigo_evento.imagem_banner and antigo_evento.imagem_banner != instance.imagem_banner:
            try:
                cloudinary.uploader.destroy(antigo_evento.imagem_banner.public_id)
            except Exception as e:
                print(f"Erro ao deletar banner antigo do Cloudinary: {e}")