import numpy as np
from sentence_transformers import SentenceTransformer
import json
import pickle
import os

class RoadSafetyEmbeddingPipeline:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.embedding_model = SentenceTransformer(model_name)
        self.vector_db_path = "./road_safety_index.pkl"
        self.data = []
        self.embeddings = None
        if os.path.exists(self.vector_db_path):
            self.load_database()
    
    def load_json_data(self, json_file_path):
        try:
            with open(json_file_path, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def add_interventions_to_db(self, interventions_data):
        if not interventions_data:
            return False
        self.data = interventions_data
        texts = [self._create_composite_text(i) for i in self.data]
        self.embeddings = self.embedding_model.encode(texts)
        self.save_database()
        return True
    
    def _create_composite_text(self, intervention):
        # Handle both old and new data formats
        # New format: problem, category, type, data, code, clause, content
        # Old format: name, description, problem_type, road_type, effectiveness, cost
        
        # Extract name/type
        name = intervention.get('name') or intervention.get('type', '')
        
        # Extract description/data
        description = intervention.get('description') or intervention.get('data', '')
        
        # Extract problem - could be string or list
        problem = intervention.get('problem', '')
        if isinstance(problem, list):
            problem_types = ', '.join(problem)
        elif problem:
            problem_types = problem
        else:
            problem_types = ', '.join(intervention.get('problem_type', []))
        
        # Extract category
        category = intervention.get('category', '')
        
        # Extract code and clause
        code = intervention.get('code', '')
        clause = intervention.get('clause', '')
        
        # Extract content if available
        content = intervention.get('content', '')
        
        # Build composite text for embedding
        parts = [
            f"Intervention: {name}",
            f"Category: {category}",
            f"Problem: {problem_types}",
            f"Description: {description}",
            f"Code: {code}",
            f"Clause: {clause}"
        ]
        
        if content:
            parts.append(f"Content: {content}")
        
        # Add old format fields if present
        road_types = intervention.get('road_type', [])
        if road_types:
            parts.append(f"Road Types: {', '.join(road_types) if isinstance(road_types, list) else road_types}")
        
        effectiveness = intervention.get('effectiveness', '')
        if effectiveness:
            parts.append(f"Effectiveness: {effectiveness}")
        
        cost = intervention.get('cost', '')
        if cost:
            parts.append(f"Cost: {cost}")
        
        return " ".join(parts)
    
    def search_interventions(self, query, top_k=5):
        if self.embeddings is None:
            return {'interventions': [], 'total_count': 0}
        query_embedding = self.embedding_model.encode([query])
        similarities = np.dot(self.embeddings, query_embedding.T).flatten()
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = {'interventions': []}
        for i, idx in enumerate(top_indices):
            intervention = self.data[idx]
            
            # Handle both old and new data formats
            name = intervention.get('name') or intervention.get('type', '')
            description = intervention.get('description') or intervention.get('data', '')
            
            # Handle problem - could be string or list
            problem = intervention.get('problem', '')
            if isinstance(problem, str) and problem:
                problem_type = [problem]
            elif isinstance(problem, list):
                problem_type = problem
            else:
                problem_type = intervention.get('problem_type', [])
            
            # Get other fields
            category = intervention.get('category', '')
            road_type = intervention.get('road_type', [])
            if not road_type:
                # Try to infer from category
                if category:
                    road_type = [category]
            
            results['interventions'].append({
                'rank': i + 1,
                'name': name,
                'problem_type': problem_type if isinstance(problem_type, list) else [problem_type] if problem_type else [],
                'road_type': road_type if isinstance(road_type, list) else [road_type] if road_type else [],
                'similarity_score': round(float(similarities[idx]), 3),
                'description': description,
                'category': category,
                'code': intervention.get('code', ''),
                'clause': intervention.get('clause', ''),
                'type': intervention.get('type', ''),
                'problem': intervention.get('problem', ''),
                'data': intervention.get('data', ''),
                'content': intervention.get('content', ''),
                'S. No.': intervention.get('S. No.', '')
            })
        results['total_count'] = len(results['interventions'])
        return results
    
    def save_database(self):
        with open(self.vector_db_path, 'wb') as f:
            pickle.dump({'data': self.data, 'embeddings': self.embeddings}, f)
    
    def load_database(self):
        try:
            with open(self.vector_db_path, 'rb') as f:
                saved_data = pickle.load(f)
                self.data = saved_data['data']
                self.embeddings = saved_data['embeddings']
        except:
            self.data = []
            self.embeddings = None
