from django.core.mail import send_mail

send_mail(
    "Teste Django",
    "Este é um e-mail de teste enviado pelo Django.",
    "projeto.tcc.getulio@gmail.com",
    ["getuliojose01@gmail.com"],
    fail_silently=False,
)
