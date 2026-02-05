# Styles CSS pour l'interface Streamlit

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600&family=Spectral:wght@400;600&display=swap');

:root {
    --ink: #0f172a;
    --accent: #0b4f6c;
    --accent-2: #1985a1;
    --paper: #f7f9fc;
    --gold: #f2d492;
}

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

.main {
    background: radial-gradient(1200px 600px at 10% -10%, #eef5ff 0%, transparent 60%),
                radial-gradient(800px 400px at 90% 10%, #f7f1e1 0%, transparent 55%),
                var(--paper);
}

.block-container {
    padding-top: 2.5rem;
}

.hero {
    background: linear-gradient(120deg, #ffffff 0%, #f2f7ff 100%);
    border-radius: 18px;
    padding: 24px 28px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    margin-bottom: 20px;
}

.hero h1 {
    font-family: 'Spectral', serif;
    margin: 0 0 6px 0;
    color: var(--ink);
}

.hero p {
    margin: 0;
    color: #475569;
}

.section-title {
    font-family: 'Spectral', serif;
    font-weight: 600;
    margin-top: 8px;
    color: var(--ink);
}

.stButton > button {
    background: var(--accent);
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    border: none;
    font-weight: 600;
}

.stButton > button:hover {
    background: var(--accent-2);
    color: white;
}

.card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
}

.result-card {
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
    border: 1px solid #dbe7f3;
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
}

.badge {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.85rem;
}

.badge-success {
    background: #e8f5e9;
    color: #1b5e20;
    border: 1px solid #c8e6c9;
}

.badge-danger {
    background: #ffebee;
    color: #b71c1c;
    border: 1px solid #ffcdd2;
}

.badge-info {
    background: #eef2ff;
    color: #1e3a8a;
    border: 1px solid #c7d2fe;
}

.small-note {
    color: #64748b;
    font-size: 0.9rem;
}
</style>
"""
