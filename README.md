# imagen

Generative AI image use case demos.

Uses a mix of local and API-based LLMs and other generative AI services to generate, describe, and search through an image library.

Originally forked from [this project](https://github.com/onepointconsulting/image_search) from Onepoint Consulting.

## Install

### Project

Imagen uses [hatch](https://hatch.pypa.io/latest/) as its project manager and should be installed first.

If you just want to run the project on its own, you don't need to worry about installing any other Python dependencies. Hatch will handle it.

### Models

There are two groups of models currently impplemented: local and remote. The project needs an OpenAI API token in the environment (export or .env) to function. ## docs here

For local models, this project uses [Ollama]() as the host. Once installed, run these commands to download and serve the models.

```bash
ollama pull llava:latest
ollama pull nomic-embed-text:latest
ollama serve
```

## Run

```bash
hatch run serve:start
```

```bash
hatch run app:start
```

## Develop

```bash
hatch fmt
```

```bash
hatch run types:check
```

## Tests

```bash
hatch test
```

## CLI

