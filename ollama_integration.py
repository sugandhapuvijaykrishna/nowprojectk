import subprocess
import json
import os
from embedding_pipeline import RoadSafetyEmbeddingPipeline

class RoadSafetyRAG:
    def __init__(self):
        self.pipeline = RoadSafetyEmbeddingPipeline()
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.2:3b')
    
    def query_ollama(self, prompt):
        """Query Ollama LLM with improved error handling"""
        try:
            # Try using ollama Python client first (if installed)
            try:
                import ollama
                response = ollama.generate(model=self.ollama_model, prompt=prompt)
                return response.get('response', '').strip()
            except ImportError:
                # Fallback to subprocess
                result = subprocess.run(
                    ['ollama', 'run', self.ollama_model, prompt],
                    capture_output=True, text=True, timeout=60
                )
                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    return f"Ollama error: {result.stderr}"
        except subprocess.TimeoutExpired:
            return "Ollama request timed out. Please try again with a shorter query."
        except FileNotFoundError:
            return "Ollama is not installed or not in PATH. Please install Ollama from https://ollama.ai"
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}. Please ensure Ollama is running."
    
    def get_recommendations(self, user_query, top_k=3):
        """Get AI-powered recommendations based on retrieved interventions"""
        retrieved = self.pipeline.search_interventions(user_query, top_k=top_k)
        
        if not retrieved['interventions']:
            return {
                "query": user_query,
                "retrieved_interventions": [],
                "recommendation": "No relevant interventions found for your query. Please try rephrasing or upload more intervention data."
            }
        
        # Build comprehensive context
        context_parts = []
        for i, item in enumerate(retrieved['interventions']):
            name = item.get('name', 'N/A')
            description = item.get('description', 'N/A')
            problem_types = item.get('problem_type', [])
            if not problem_types:
                problem = item.get('problem', '')
                if problem:
                    problem_types = [problem]
            
            problem_str = ', '.join(problem_types) if problem_types else 'N/A'
            category = item.get('category', '')
            code = item.get('code', '')
            clause = item.get('clause', '')
            
            context_parts.append(
                f"{i+1}. {name}\n"
                f"   - Category: {category if category else 'N/A'}\n"
                f"   - Problem: {problem_str}\n"
                f"   - Description: {description}\n"
                f"   - Code: {code if code else 'N/A'}\n"
                f"   - Clause: {clause if clause else 'N/A'}\n"
                f"   - Similarity Score: {item.get('similarity_score', 0):.3f}"
            )
        
        context = "\n\n".join(context_parts)
        
        prompt = f"""You are an expert road safety consultant with deep knowledge of IRC codes and road safety standards. 

User Query: "{user_query}"

Based on the following relevant road safety interventions retrieved from the database, provide a detailed, actionable recommendation:

{context}

Please provide a comprehensive response that includes:

1. **Recommended Solution**: Clearly state which intervention(s) from the list above best addresses the user's query. Reference the specific intervention by name/type.

2. **Why This Solution**: Explain in detail why this intervention is suitable for the specific problem mentioned in the query. Reference the technical details (code, clause) provided.

3. **Implementation Details**: Based on the intervention data provided, explain:
   - Key specifications and requirements
   - Placement/installation guidelines if mentioned
   - Dimensions, materials, or technical standards if applicable

4. **Important Considerations**: Mention any critical factors from the intervention data such as:
   - Road type requirements
   - Speed considerations
   - Visibility requirements
   - Maintenance needs

5. **Expected Results**: What outcomes can be expected from implementing this solution based on the intervention standards.

6. **Alternative Options**: If other interventions from the list could also work, mention them briefly.

Format your response in clear, professional language suitable for road safety planning. Be specific and reference the intervention details provided. Use bullet points for clarity."""

        response = self.query_ollama(prompt)
        
        # Enhance retrieved interventions with full data
        enhanced_interventions = []
        for item in retrieved['interventions']:
            # Find full intervention data - match by name or type
            full_data = None
            for i in self.pipeline.data:
                if (i.get('name') == item.get('name') or 
                    i.get('type') == item.get('name') or
                    i.get('type') == item.get('type')):
                    full_data = i
                    break
            
            if not full_data:
                full_data = item
            
            # Build enhanced item with all available fields
            enhanced_item = {
                **item,
                'description': full_data.get('description') or full_data.get('data', item.get('description', 'N/A')),
                'effectiveness': full_data.get('effectiveness', 'N/A'),
                'cost': full_data.get('cost', 'N/A'),
                'implementation_time': full_data.get('implementation_time', 'N/A'),
                'intervention_id': full_data.get('intervention_id') or full_data.get('S. No.', 'N/A'),
                'category': full_data.get('category', item.get('category', 'N/A')),
                'code': full_data.get('code', item.get('code', 'N/A')),
                'clause': full_data.get('clause', item.get('clause', 'N/A')),
                'type': full_data.get('type', item.get('type', 'N/A')),
                'problem': full_data.get('problem', item.get('problem', 'N/A'))
            }
            enhanced_interventions.append(enhanced_item)
        
        return {
            "query": user_query,
            "retrieved_interventions": enhanced_interventions,
            "recommendation": response
        }