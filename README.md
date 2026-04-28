# Stoq PRO v2.2

Pacote PWA completo para GitHub Pages.

## Arquivos essenciais
- `index.html` — app completo
- `manifest.json` — configuração PWA
- `sw.js` — service worker/offline/cache
- `icons/` — ícones do app
- `splash/` — imagens de splash iOS
- `instalar_pc_windows.bat` — auxiliar de instalação no Windows
- `instalar_mobile.txt` — instruções Android/iPhone

## Como publicar
1. Suba todos os arquivos para o repositório `stoq` no GitHub.
2. Ative o GitHub Pages na branch principal.
3. Acesse `https://ceducunha-alt0609.github.io/stoq/`.
4. Instale pelo navegador.

## Observação
O app só instala como PWA real via HTTPS. Abrir por `file://` serve para teste visual, mas não ativa service worker nem instalação completa.
