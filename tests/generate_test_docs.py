from pathlib import Path

def create_sample_docs(dest_path: str):
    """
    Creates a sample Markdown developer documentation file for testing.
    """
    content = """# FastAPI Dependency Injection

FastAPI has a very powerful Dependency Injection system that is easy to use and integrates seamlessly.

## Declaring Dependencies
You can import `Depends` from `fastapi` and use it inside your path operation functions.

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

## Deprecation Notice
The old `fastapi.dependencies` layout is deprecated since version 0.95.0. Use standard `Depends` instead.
    """
    path = Path(dest_path)
    path.parent.mkdir(exist_ok=True, parents=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Sample documentation file created at {dest_path}")

if __name__ == "__main__":
    import sys
    dest = Path(__file__).parent.parent / "data" / "fastapi_di.md"
    create_sample_docs(str(dest))
