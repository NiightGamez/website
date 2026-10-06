# mvoorhies.com - Personal Portfolio & Engineering Workbench

The source code and infrastructure configuration powering [mvoorhies.com](https://mvoorhies.com).
Built with Astro, styled with Tailwind CSS, and self-hosted on Proxmox VE behind Cloudflare Zero Trust.

## Architecture & Hosting
* **Ingress:** Cloudflare Edge / Zero Trust WAF
* **Tunnel:** Encrypted Outbound Argo Tunnel (cloudflared)
* **Host:** Proxmox VE Hypervisor
* **Container:** CT-102 (Debian 12 LXC)
* **Web Server:** Nginx (Reverse Proxy & Hardened CSP Headers)

## Features
* Retro-terminal aesthetic with monospace styling and ASCII art
* Interactive Command Palette (Ctrl + K)
* Dynamic GitHub repository ingestion for /portfolio
* Self-hosted Immich photography integration

## License
MIT License
