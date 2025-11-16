"""Test the RAG pipeline to ensure it's working correctly"""
from embedding_pipeline import RoadSafetyEmbeddingPipeline
from ollama_integration import RoadSafetyRAG
import json
import sys

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("Testing RAG Pipeline")
print("=" * 60)

# Load data
print("\n1. Loading interventions.json...")
with open('interventions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(f"   [OK] Loaded {len(data)} interventions")

# Test embedding pipeline
print("\n2. Testing embedding pipeline...")
pipeline = RoadSafetyEmbeddingPipeline()
pipeline.add_interventions_to_db(data)
print(f"   [OK] Created embeddings for {len(pipeline.data)} interventions")

# Test search
print("\n3. Testing search functionality...")
test_queries = [
    "damaged stop sign",
    "speed hump requirements",
    "missing road markings",
    "height issue with signs"
]

for query in test_queries:
    print(f"\n   Query: '{query}'")
    results = pipeline.search_interventions(query, top_k=3)
    print(f"   Found {len(results['interventions'])} results:")
    for item in results['interventions']:
        print(f"      - {item['name']} (score: {item['similarity_score']:.4f})")

# Test full RAG system
print("\n4. Testing full RAG system with Ollama...")
rag = RoadSafetyRAG()
rag.pipeline = pipeline

test_query = "How to fix a damaged STOP sign?"
print(f"\n   Query: '{test_query}'")
print("   Generating recommendation...")

try:
    result = rag.get_recommendations(test_query, top_k=3)
    print(f"\n   [OK] Retrieved {len(result['retrieved_interventions'])} interventions")
    print(f"   [OK] Generated recommendation: {len(result['recommendation'])} characters")
    print("\n   Recommendation preview:")
    print("   " + "-" * 56)
    print("   " + result['recommendation'][:200] + "...")
    print("   " + "-" * 56)
except Exception as e:
    print(f"   [ERROR] Error: {e}")

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)

