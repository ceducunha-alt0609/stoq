# Stoq — pacote PWA completo

Este pacote está pronto para publicar e instalar como app no **PC**, **Android** e **iPhone/iPad**.

## Estrutura

- `index.html`
- `manifest.json`
- `sw.js`
- `offline.html`
- `404.html`
- `robots.txt`
- `browserconfig.xml`
- `icons/`
- `splash/`

## Como instalar corretamente

O PWA precisa rodar em:

- `https://` em produção, ou
- `http://localhost` em teste local

Abrir por `file://` normalmente faz o navegador criar apenas um atalho, sem recursos completos do app.

## Teste local rápido

### Python

```bash
python -m http.server 8080
```

Depois abra:

```bash
http://localhost:8080
```

## Publicação simples

Você pode subir esta pasta em:

- GitHub Pages
- Netlify
- Vercel
- servidor próprio com HTTPS

## O que já está configurado

- instalação standalone
- cache offline básico
- tela offline
- ícones principais
- splash para Apple
- suporte básico a Windows tile
- arquivos auxiliares para deploy

## Observações

Se trocar arquivos importantes e o navegador insistir na versão antiga:

1. atualize a página
2. feche e abra o app
3. se necessário, desinstale e instale novamente
4. em último caso, limpe os dados do site
