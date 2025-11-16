from ollama_integration import RoadSafetyRAG
import json

def main():
    rag_system = RoadSafetyRAG()
    
    sample_data = [
        {
            'intervention_id': 'RSI-001',
            'name': 'Speed Humps',
            'description': 'Vertical deflection devices that physically slow vehicles by creating discomfort at higher speeds. Effective in residential areas and school zones.',
            'problem_type': ['speeding', 'residential safety', 'pedestrian safety'],
            'road_type': ['local streets', 'school zones', 'residential areas'],
            'effectiveness': 'High',
            'cost': 'Low to Medium',
            'implementation_time': '1-2 weeks'
        },
        {
            'intervention_id': 'RSI-002',
            'name': 'Roundabouts', 
            'description': 'Circular intersections that reduce conflict points and slow traffic speeds while maintaining traffic flow.',
            'problem_type': ['intersection crashes', 'high-speed crashes', 'angle collisions'],
            'road_type': ['intersections', 'rural highways', 'urban arterials'],
            'effectiveness': 'Very High', 
            'cost': 'High',
            'implementation_time': '3-6 months'
        },
        {
            'intervention_id': 'RSI-003',
            'name': 'Pedestrian Crosswalks',
            'description': 'Marked crosswalks with enhanced visibility features like flashing lights or raised platforms.',
            'problem_type': ['pedestrian safety', 'crossing accidents', 'visibility issues'],
            'road_type': ['urban roads', 'commercial areas', 'school zones'],
            'effectiveness': 'Medium',
            'cost': 'Low',
            'implementation_time': '1-3 weeks'
        },
        {
            'intervention_id': 'RSI-004',
            'name': 'Guardrails',
            'description': 'Barrier systems that prevent vehicles from leaving the roadway in critical areas.',
            'problem_type': ['run-off-road crashes', 'roadside hazards', 'bridge approaches'],
            'road_type': ['highways', 'mountain roads', 'curves'],
            'effectiveness': 'High',
            'cost': 'Medium to High',
            'implementation_time': '2-4 weeks'
        }
    ]
    
    rag_system.pipeline.add_interventions_to_db(sample_data)
    
    test_queries = [
        "How to reduce speeding in residential areas near a school?",
        "What are cost-effective solutions for pedestrian safety?",
        "How to prevent intersection crashes on busy roads?",
        "Solutions for run-off-road accidents on highways"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"QUERY: {query}")
        print(f"{'='*60}")
        
        result = rag_system.get_recommendations(query)
        
        print("\nRETRIEVED INTERVENTIONS:")
        for intervention in result['retrieved_interventions']:
            print(f"  - {intervention['name']} (Score: {intervention['similarity_score']})")
            print(f"    Problems: {', '.join(intervention['problem_type'])}")
            print(f"    Road Types: {', '.join(intervention['road_type'])}")
        
        print(f"\nRECOMMENDATION:")
        print(result['recommendation'])
        print(f"{'='*60}")

if __name__ == '__main__':
    main()