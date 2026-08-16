# DocRAG — Geliştirici Dokümantasyon Asistanı

[English](README.md) | [Türkçe](README_TR.md)

DocRAG; HTML, Markdown ve PDF biçimindeki yazılım dokümantasyonlarını ayrıştıran, anlamsal arama yapan, kurulum ve hata sorularını yanıtlayan ve çalıştırılabilir kod örnekleri üreten geliştirici odaklı bir RAG sistemidir.

## Teknolojiler

- FastAPI ve Uvicorn arka ucu
- ChromaDB ve Gemini embeddings
- Gemini dil modeli
- BeautifulSoup, Markdown ve PyMuPDF ayrıştırıcıları
- Streamlit arayüzü

## Kurulum

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="api_anahtariniz"
```

API anahtarı yoksa uygulama çevrimdışı testler için örnek yanıt modunda çalışır.

## Çalıştırma

Arka uç:

```bash
python -m backend.main
```

API `http://127.0.0.1:8003`, OpenAPI belgeleri ise `/docs` adresinde açılır.

Arayüz:

```bash
streamlit run frontend/app.py
```

## Testler

```bash
pytest tests/
```

