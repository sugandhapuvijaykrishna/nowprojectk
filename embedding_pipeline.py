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
        # Encode with normalization for better cosine similarity
        self.embeddings = self.embedding_model.encode(texts, normalize_embeddings=True)
        self.save_database()
        return True
    
    def _create_composite_text(self, intervention):
        # Handle both old and new data formats
        # New format: problem, category, type, data, code, clause, content
        # Old format: name, description, problem_type, road_type, effectiveness, cost
        
        # Extract name/type - prioritize type as it's more specific
        name = intervention.get('type', '') or intervention.get('name', '')
        
        # Extract description/data - use data field which has more detail
        description = intervention.get('data', '') or intervention.get('description', '')
        
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
        
        # Extract content if available - this has the full formatted text
        content = intervention.get('content', '')
        
        # Build comprehensive composite text for better embeddings
        # Include all relevant information that users might search for
        parts = []
        
        # Primary identifiers
        if name:
            parts.append(f"{name}")
        if category:
            parts.append(f"{category}")
        if problem_types:
            parts.append(f"{problem_types}")
        
        # Detailed description - use content if available as it's more comprehensive
        if content:
            parts.append(content)
        elif description:
            parts.append(description)
        
        # Technical details
        if code:
            parts.append(f"Code {code}")
        if clause:
            parts.append(f"Clause {clause}")
        
        # Add old format fields if present
        road_types = intervention.get('road_type', [])
        if road_types:
            road_str = ', '.join(road_types) if isinstance(road_types, list) else str(road_types)
            parts.append(f"Road types: {road_str}")
        
        effectiveness = intervention.get('effectiveness', '')
        if effectiveness:
            parts.append(f"Effectiveness: {effectiveness}")
        
        cost = intervention.get('cost', '')
        if cost:
            parts.append(f"Cost: {cost}")
        
        # Join with spaces for better embedding
        return " ".join(parts)
    
    def search_interventions(self, query, top_k=5, min_similarity=0.3):
        if self.embeddings is None or len(self.data) == 0:
            return {'interventions': [], 'total_count': 0}
        
        # Encode query
        query_embedding = self.embedding_model.encode([query], normalize_embeddings=True)
        
        # Normalize embeddings for better cosine similarity
        if self.embeddings is not None:
            # Normalize embeddings
            norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
            normalized_embeddings = self.embeddings / (norms + 1e-8)
            
            # Calculate cosine similarity
            similarities = np.dot(normalized_embeddings, query_embedding.T).flatten()
        else:
            return {'interventions': [], 'total_count': 0}
        
        # Get top k indices, but filter by minimum similarity
        top_indices = np.argsort(similarities)[::-1][:top_k * 2]  # Get more candidates
        filtered_indices = [idx for idx in top_indices if similarities[idx] >= min_similarity][:top_k]
        
        if not filtered_indices:
            # If no results meet threshold, return top results anyway
            filtered_indices = top_indices[:top_k]
        
        results = {'interventions': []}
        for i, idx in enumerate(filtered_indices):
            intervention = self.data[idx]
            
            # Handle both old and new data formats
            name = intervention.get('type', '') or intervention.get('name', '')
            description = intervention.get('data', '') or intervention.get('description', '')
            
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
                'similarity_score': round(float(similarities[idx]), 4),
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
