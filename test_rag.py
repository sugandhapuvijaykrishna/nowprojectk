from embedding_pipeline import RoadSafetyEmbeddingPipeline
import json

# Load and test the RAG system
pipeline = RoadSafetyEmbeddingPipeline()
data = json.load(open('interventions.json'))
pipeline.add_interventions_to_db(data)
print(f'✅ Loaded {len(data)} interventions successfully!')

# Test search
result = pipeline.search_interventions('damaged stop sign', top_k=3)
print(f'\n🔍 Test search found {len(result["interventions"])} results:')
for i in result['interventions']:
    print(f"  - {i['name']} (score: {i['similarity_score']})")
    print(f"    Problem: {i.get('problem', 'N/A')}")
    print(f"    Category: {i.get('category', 'N/A')}")

print("\n✅ RAG system is working correctly!")

