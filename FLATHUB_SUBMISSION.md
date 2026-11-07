# Flathub Submission Runbook

> Estado: repositório pronto para submissão. Este arquivo é o passo a passo
> manual — o PR no `flathub/flathub` precisa ser aberto **por um humano**
> (a política do Flathub proíbe PRs de submissão abertos por agentes de IA,
> e o `bot, build` deve ser comentado pela sua conta).

## Pré-requisitos

- Conta GitHub com 2FA ativado (`alesima`).
- Tag `v1.1.0` publicada neste repositório (o manifesto aponta para ela).
- App ID final: `io.github.alesima.eisenhower`
  (`com.github.*` é reservado e seria rejeitado — já migrado).

## 1. Publicar a release

```bash
cd /home/alex/Projects/Personal/eisenhower
git tag v1.1.0
git push origin main v1.1.0
gh release create v1.1.0 --title "v1.1.0 Flathub-ready" \
  --notes-file CHANGELOG.md
```

## 2. Conferir o build a partir do manifesto final

O manifesto usa `type: git` + `tag: v1.1.0`, então só compila após o push:

```bash
flatpak-builder --user --install --force-clean build-dir \
  io.github.alesima.eisenhower.yml
flatpak run io.github.alesima.eisenhower
flatpak run --command=flatpak-builder-lint org.flatpak.Builder \
  manifest io.github.alesima.eisenhower.yml
```

## 3. Abrir o PR de submissão

```bash
# 1. Fork https://github.com/flathub/flathub DESMARCANDO
#    "Copy the master branch only" (precisa do branch new-pr).
# 2. Clonar o fork já no branch new-pr:
git clone --branch=new-pr git@github.com:alesima/flathub.git /tmp/flathub-fork
cd /tmp/flathub-fork
git checkout -b add-eisenhower-matrix new-pr
mkdir io.github.alesima.eisenhower
cp /home/alex/Projects/Personal/eisenhower/io.github.alesima.eisenhower.yml \
   io.github.alesima.eisenhower/
cp /home/alex/Projects/Personal/eisenhower/flathub.json \
   io.github.alesima.eisenhower/
git add io.github.alesima.eisenhower
git commit -m "Add io.github.alesima.eisenhower"
git push origin add-eisenhower-matrix
```

Abrir o PR **contra o branch `new-pr`** (nunca `master`) com título
`Add io.github.alesima.eisenhower` e comentar `bot, build` para o build de teste.

## 4. Pós-aprovação

- Aceitar o convite para `flathub/io.github.alesima.eisenhower` em até 1 semana.
- Atualizações futuras: push de tag nova + bump do `tag:` no manifesto do
  repositório Flathub (sem novo processo de submissão).
- Verificação (selo azul): https://flathub.org → perfil → "Verify"
  via token em `https://github.com/alesima` (domínio) ou login GitHub.

## 5. Loja do GNOME

Não há "upload" separado: o GNOME Software lista automaticamente apps do
Flathub. Após a publicação, "Eisenhower Matrix" aparece pesquisável no
GNOME Software. (O catálogo curado `apps.gnome.org`/GNOME Circle é um
processo separado e opcional, que exige publicação prévia no Flathub.)
