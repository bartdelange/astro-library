# Astro Library

<p align="center">
  <img src="frontend/public/favicon.svg" alt="Astro Library" width="128">
</p>

<h3 align="center">
A self-hosted astrophotography library for organizing, exploring and reliving your imaging journey.
</h3>

<p align="center">
  <a href="https://github.com/bartdelange/astro-library/releases">
    <img src="https://img.shields.io/github/v/release/bartdelange/astro-library?style=for-the-badge" alt="Latest Release">
  </a>
  <a href="https://github.com/bartdelange/astro-library/pkgs/container/astro-library">
    <img src="https://img.shields.io/badge/Container-GHCR-blue?style=for-the-badge&logo=docker" alt="Container Registry">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  </a>
  <img src="https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
</p>

<p align="center">
  <a href="https://github.com/sponsors/bartdelange">
    <img src="https://img.shields.io/badge/GitHub%20Sponsors-support-EA4AAA?style=for-the-badge&logo=github-sponsors&logoColor=white" alt="GitHub Sponsors">
  </a>
  <a href="https://ko-fi.com/bartdelange">
    <img src="https://img.shields.io/badge/Ko--fi-support-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white" alt="Ko-fi">
  </a>
</p>

---

Astro Library is an open-source application that helps astrophotographers organize their complete imaging archive. Instead of focusing on image acquisition or processing, Astro Library focuses on what comes afterwards: preserving, enriching and browsing your work in a structured way.

Whether you've captured a handful of images or built an archive spanning thousands of sessions, Astro Library provides a central place to explore your astrophotography history.

---

## Why?

Most astrophotographers have images scattered across folders, external drives and processing software.

```text
M31/
    Final/
    PixInsight/
    Siril/
    Lights/
    Calibration/
```

While this works, it quickly becomes difficult to answer questions like:

- When did I image this object?
- How much total integration time do I have?
- Which telescope or camera did I use?
- Which version became my final image?
- What did this object look like before I reprocessed it?
- Which targets have I already photographed?
- What should I image next?

Astro Library indexes your existing library and turns it into something you can browse, search and enjoy.

The goal is simple:

> Spend less time digging through folders, and more time looking back at everything you've captured.

---

## Features

### 📚 Structured library

Browse your complete astrophotography collection by object, project and imaging session.

Instead of navigating folders, explore your library using meaningful metadata.

### 🔭 Metadata enrichment

Automatically enrich your objects using astronomical databases including:

- SIMBAD
- VizieR
- NED

Additional metadata makes your library significantly more informative while keeping your original files untouched.

### 🖼 Image browser

View your processed images alongside their associated sessions, source data and metadata.

Hero images make it easy to quickly recognize each object throughout the application.

### 📈 Timeline

Explore your astrophotography journey over time.

See when objects were captured, revisited or reprocessed, and follow your progression as an astrophotographer.

### 🌌 FITS support

Browse FITS files directly from your library.

Support for richer FITS visualization is planned without requiring external software.

### 🎯 Planning

Discover what you've already photographed, what still needs more integration time and which targets are good candidates for your next clear night.

---

## Philosophy

Astro Library does **not** replace your capture or processing software.

Instead, it complements the tools you already use.

Whether your workflow involves Siril, PixInsight, GraXpert, Photoshop or something entirely different, Astro Library aims to organize the results—not dictate how you create them.

Your files remain yours.

The application indexes and enriches your library rather than forcing you into a proprietary format or workflow.

---

## Project Structure

Astro Library models an astrophotography archive using four core concepts:

```text
Object
└── Project
    └── Session
        └── Files
```

- **Objects** represent astronomical targets.
- **Projects** group work on an object.
- **Sessions** represent individual imaging nights.
- **Files** contain everything associated with those sessions, from raw captures to processed exports.

This structure allows multiple processing workflows, multiple revisions and multiple imaging sessions to coexist naturally.

---

## Technology

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite (currently)

### Frontend

- React
- TypeScript
- Vite

### Deployment

Designed to run as a self-hosted application using Docker.

Perfect for:

- NAS systems
- Home servers
- Mini PCs
- Dedicated observatory computers

---

## Status

Astro Library is early-stage software. It is useful for experimentation and development, but the data model, APIs and UI may still change before a stable release.

Keep backups of your astrophotography library and application data. Astro Library is designed to index and enrich your files, not to be the only copy of them.

---

## Quick Start

### Docker

```bash
docker compose -f docker/docker-compose.yml up --build
```

The app will be available at `http://localhost:8080`.

By default, the compose file stores application data in a Docker volume and mounts `example/library` read-only as the library path. Change the `ASTRO_LIBRARY_LIBRARY_DIR` environment variable and volume mount to point at your own astrophotography archive.

### Local Development

Backend:

```bash
cd backend
uv sync --all-extras --dev
cp .env.example .env
uv run uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm ci
npm run dev
```

The frontend runs through Vite and proxies `/api` requests to the backend.

### Checks

```bash
cd frontend
npm run format:check
npm run lint
npm run typecheck
npm run build
```

```bash
cd backend
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

---

## Roadmap

The long-term vision includes:

- Rich FITS viewer
- Advanced search
- Equipment tracking
- Interactive sky planning
- Public gallery sharing
- Additional metadata providers
- Performance improvements for very large libraries
- Plugin architecture

---

## Contributing

Contributions are welcome.

Bug reports, feature requests and pull requests are greatly appreciated.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

For security issues, please read [SECURITY.md](SECURITY.md).

If Astro Library is useful to you, you can support development through [GitHub Sponsors](https://github.com/sponsors/bartdelange) or [Ko-fi](https://ko-fi.com/bartdelange).

---

## Support

If you enjoy Astro Library, you can help by:

- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting features
- 🔀 Contributing code or documentation
- 📣 Sharing the project with other astrophotographers

---

## License

Astro Library is released under the [MIT License](LICENSE).
