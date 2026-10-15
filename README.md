# mvoorhies.com — Personal Portfolio & Engineering Workbench

The source code and infrastructure configuration powering [mvoorhies.com](https://mvoorhies.com), an interactive terminal-inspired portfolio and homelab showcase.

Built with **Astro**, styled with **Tailwind CSS**, and self-hosted on a Proxmox VE hypervisor behind Cloudflare Zero Trust.

---

## 🏗️ Architecture & Hosting Topology

Public ingress bypasses residential router port-forwarding using an encrypted, outbound-only tunnel terminating at an unprivileged container:

* **Edge Ingress:** Cloudflare Zero Trust WAF & TLS 1.3 Termination
* **Tunnel Agent:** `cloudflared` (encrypted outbound Argo tunnel)
* **Hypervisor Node:** Proxmox VE
* **Compute Host:** CT-102 (Unprivileged Debian 12 LXC)
* **Web Server:** Nginx (Static asset delivery with custom security headers)
* **Static Engine:** Astro (Static Site Generation)

---

## 🔒 Security & System Hardening

* **Zero Inbound Port Forwarding:** Ingress strictly operates via outbound Cloudflare Tunnels, keeping public IP addresses unexposed.
* **Network Isolation:** Proxmox host firewall rules drop lateral egress connections to private RFC 1918 subnets.
* **Hardened Headers:** Enforces Content Security Policy (CSP), frame options, and strict MIME sniffing boundaries.

---

## 📜 License & Terms of Use

This repository uses a hybrid licensing model to balance open-source education with personal copyright protection:

* **Source Code Scaffolding:** The underlying framework code, boilerplate components, and utility build scripts are available under the **MIT License**. You are free to reference, study, and adapt the technical mechanisms for educational and non-commercial purposes.
* **Personal Identity, Design & Content (All Rights Reserved):** 
  * All personal photography, gallery media, written write-ups, homelab documentation, and distinct visual layout identity are **© 2026 Michael Voorhies. All Rights Reserved.**
  * You may **not** copy, re-host, mirror, or redistribute the photography, design assets, or biographical identity for your own website, public portfolio, or commercial purposes without explicit prior written authorization.
