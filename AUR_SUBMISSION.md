# AUR Submission Runbook

> Estado: pacote validado localmente com `makepkg -s` (1.1.0-1 constrói limpo,
> checksum fixado, desktop/metainfo/ícone/licença nos caminhos corretos).
> Falta apenas o push para `aur.archlinux.org`, que exige conta no AUR + chave
> SSH — o push **precisa ser feito por você** (este ambiente não tem sua chave).

## Pré-requisitos (só na primeira vez)

1. Criar conta em https://aur.archlinux.org/register
2. Gerar chave SSH e cadastrar em https://aur.archlinux.org/account:
   ```bash
   ssh-keygen -t ed25519 -C "aur@alesima" -f ~/.ssh/aur
   # adicionar ~/.ssh/aur.pub no perfil do AUR
   ```
   ```
   # ~/.ssh/config
   Host aur.archlinux.org
     IdentityFile ~/.ssh/aur
     User aur
   ```
3. Testar: `ssh aur@aur.archlinux.org help` (deve listar comandos, não negar).

## Primeira submissão

```bash
git clone ssh://aur@aur.archlinux.org/eisenhower-matrix.git ~/aur/eisenhower-matrix
cd ~/aur/eisenhower-matrix
cp /home/alex/Projects/Personal/eisenhower/PKGBUILD .
cp /home/alex/Projects/Personal/eisenhower/.SRCINFO .
git add PKGBUILD .SRCINFO
git commit -m "Initial submission of eisenhower-matrix 1.1.0"
git push origin master
```

Depois do push, o pacote aparece em
https://aur.archlinux.org/packages/eisenhower-matrix e instala via:

```bash
yay -S eisenhower-matrix
```

(não existe "publicar no yay": o yay é só um helper que instala do AUR.)

## Atualizações

```bash
cd /home/alex/Projects/Personal/eisenhower
# 1. bump pkgver no PKGBUILD (e pkgrel=1)
# 2. novo sha256: makepkg -g >> PKGBUILD (ou curl + sha256sum)
makepkg --printsrcinfo > .SRCINFO
cp PKGBUILD .SRCINFO ~/aur/eisenhower-matrix/
cd ~/aur/eisenhower-matrix
git commit -am "Update to 1.2.0" && git push origin master
```

## Validação local (já feita para 1.1.0)

```bash
mkdir /tmp/aurtest && cp PKGBUILD /tmp/aurtest/ && cd /tmp/aurtest
makepkg -s --noconfirm   # compila sem instalar
```
