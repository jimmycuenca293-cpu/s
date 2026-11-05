from PIL import Image
A='/home/user/s/app-servicio-tecnico-latam/site/img/mabe/'
CR='/home/user/s/servicio-tecnico-mabe-costa-rica/images/'
prod={'nevera-superior-negra':A+'neveras-1.jpg','nevera-superior-inox':A+'neveras-2.jpg','nevera-side-by-side':A+'neveras-0.jpg','nevera-side-by-side-inox':A+'neveras-3.jpg',
'lavadora-superior':A+'lavadoras-0.jpg','secadora':A+'secadoras-0.jpg','secadora-oscura':A+'secadoras-1.jpg','torre-lavado':A+'lavadoras-1.jpg',
'cocina-gas':CR+'cocinas/equipo-cocinas-costarica.jpg','horno-empotrable':CR+'hornos/equipo-hornos-costarica.jpg'}
for n,p in prod.items():
    im=Image.open(p).convert('RGB'); w,h=im.size; s=max(w,h); c=Image.new('RGB',(s,s),'white'); c.paste(im,((s-w)//2,(s-h)//2))
    for sz,suf in ((900,''),(460,'-m'),(240,'-s')):
        r=c.resize((sz,sz),Image.LANCZOS); r.save(f'img/{n}{suf}.webp','WEBP',quality=84,method=6)
ppl={'tecnico-cocina':A+'tecnico-0.jpg','tecnico-cliente':A+'tecnico-1.jpg','tecnico-puerta':A+'tecnico-4.jpg','tecnico-manos':A+'tecnico-8.jpg','nevera-cocina':A+'neveras-7.jpg'}
for n,p in ppl.items():
    im=Image.open(p).convert('RGB'); print(n,im.size)
    for w,suf in ((1000,''),(560,'-m')):
        r=im.copy(); r.thumbnail((w,w),Image.LANCZOS); r.save(f'img/{n}{suf}.webp','WEBP',quality=84,method=6)
im=Image.open(A+'tecnico-1.jpg').convert('RGB')
for w,suf in ((1024,''),(640,'-m')):
    r=im.copy(); r.thumbnail((w,w),Image.LANCZOS); r.save(f'img/portada{suf}.webp','WEBP',quality=82,method=6)
