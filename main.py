from embedding_pipeline import RoadSafetyEmbeddingPipeline

def main():
    pipeline = RoadSafetyEmbeddingPipeline()
    
    sample_data = [
        {
            'intervention_id': 'RSI-001',
            'name': 'Speed Humps',
            'description': 'Vertical deflection devices that physically slow vehicles in residential areas.',
            'problem_type': ['speeding', 'residential safety'],
            'road_type': ['local streets', 'school zones'],
            'effectiveness': 'High',
            'cost': 'Low to Medium'
        },
        {
            'intervention_id': 'RSI-002',
            'name': 'Roundabouts', 
            'description': 'Circular intersections that reduce conflict points and slow traffic speeds.',
            'problem_type': ['intersection crashes', 'high-speed crashes'],
            'road_type': ['intersections', 'rural highways'],
            'effectiveness': 'Very High', 
            'cost': 'High'
        }
    ]
    
    pipeline.add_interventions_to_db(sample_data)
    
    test_queries = [
        'How to reduce speeding in residential areas?',
        'Intersection safety solutions',
        'Pedestrian safety measures'
    ]
    
    for query in test_queries:
        print(f'Query: {query}')
        results = pipeline.search_interventions(query, top_k=2)
        for intervention in results['interventions']:
            print(f'  - {intervention["name"]} (Score: {intervention["similarity_score"]})')
        print()

if __name__ == '__main__':
    main()
