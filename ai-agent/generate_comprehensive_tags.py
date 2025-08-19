#!/usr/bin/env python3
"""
Generate comprehensive tag taxonomy with ~200 tags for better indexing
"""

import json
from pathlib import Path

def generate_comprehensive_tags():
    """Generate a comprehensive tag taxonomy"""
    
    # Core categories with extensive subcategories
    tags = []
    
    # Programming Languages (20 tags)
    languages = [
        ("python", "Python", "Python programming language"),
        ("javascript", "JavaScript", "JavaScript programming language"),
        ("typescript", "TypeScript", "TypeScript programming language"),
        ("java", "Java", "Java programming language"),
        ("csharp", "C#", "C# programming language"),
        ("cpp", "C++", "C++ programming language"),
        ("c", "C", "C programming language"),
        ("go", "Go", "Go programming language"),
        ("rust", "Rust", "Rust programming language"),
        ("php", "PHP", "PHP programming language"),
        ("ruby", "Ruby", "Ruby programming language"),
        ("kotlin", "Kotlin", "Kotlin programming language"),
        ("scala", "Scala", "Scala programming language"),
        ("swift", "Swift", "Swift programming language"),
        ("r", "R", "R statistical programming language"),
        ("matlab", "MATLAB", "MATLAB programming language"),
        ("perl", "Perl", "Perl programming language"),
        ("shell", "Shell Scripting", "Shell scripting and bash"),
        ("powershell", "PowerShell", "PowerShell scripting"),
        ("sql", "SQL", "SQL database queries")
    ]
    
    # Frameworks & Libraries (25 tags)
    frameworks = [
        ("react", "React", "React frontend framework"),
        ("vue", "Vue.js", "Vue.js frontend framework"),
        ("angular", "Angular", "Angular frontend framework"),
        ("svelte", "Svelte", "Svelte frontend framework"),
        ("nodejs", "Node.js", "Node.js runtime environment"),
        ("express", "Express.js", "Express.js web framework"),
        ("nestjs", "NestJS", "NestJS Node.js framework"),
        ("django", "Django", "Django Python web framework"),
        ("flask", "Flask", "Flask Python web framework"),
        ("fastapi", "FastAPI", "FastAPI Python framework"),
        ("spring", "Spring", "Spring Java framework"),
        ("spring-boot", "Spring Boot", "Spring Boot framework"),
        ("rails", "Ruby on Rails", "Ruby on Rails framework"),
        ("laravel", "Laravel", "Laravel PHP framework"),
        ("dotnet", ".NET", ".NET framework"),
        ("tensorflow", "TensorFlow", "TensorFlow ML framework"),
        ("pytorch", "PyTorch", "PyTorch ML framework"),
        ("pandas", "Pandas", "Pandas data manipulation"),
        ("numpy", "NumPy", "NumPy numerical computing"),
        ("scikit-learn", "Scikit-learn", "Scikit-learn ML library"),
        ("bootstrap", "Bootstrap", "Bootstrap CSS framework"),
        ("tailwind", "Tailwind CSS", "Tailwind CSS framework"),
        ("jquery", "jQuery", "jQuery JavaScript library"),
        ("d3", "D3.js", "D3.js data visualization"),
        ("three", "Three.js", "Three.js 3D graphics")
    ]
    
    # Cloud & Infrastructure (20 tags)
    cloud = [
        ("aws", "AWS", "Amazon Web Services"),
        ("azure", "Azure", "Microsoft Azure"),
        ("gcp", "Google Cloud", "Google Cloud Platform"),
        ("docker", "Docker", "Docker containerization"),
        ("kubernetes", "Kubernetes", "Kubernetes orchestration"),
        ("terraform", "Terraform", "Terraform infrastructure as code"),
        ("ansible", "Ansible", "Ansible automation"),
        ("jenkins", "Jenkins", "Jenkins CI/CD"),
        ("gitlab-ci", "GitLab CI", "GitLab CI/CD"),
        ("github-actions", "GitHub Actions", "GitHub Actions workflows"),
        ("nginx", "Nginx", "Nginx web server"),
        ("apache", "Apache", "Apache HTTP server"),
        ("redis", "Redis", "Redis caching"),
        ("elasticsearch", "Elasticsearch", "Elasticsearch search"),
        ("mongodb", "MongoDB", "MongoDB database"),
        ("postgresql", "PostgreSQL", "PostgreSQL database"),
        ("mysql", "MySQL", "MySQL database"),
        ("kafka", "Apache Kafka", "Apache Kafka streaming"),
        ("rabbitmq", "RabbitMQ", "RabbitMQ messaging"),
        ("microservices", "Microservices", "Microservices architecture")
    ]
    
    # AI & ML Specific (25 tags)
    ai_ml = [
        ("machine-learning", "Machine Learning", "Machine learning algorithms"),
        ("deep-learning", "Deep Learning", "Deep learning neural networks"),
        ("nlp", "Natural Language Processing", "NLP and text processing"),
        ("computer-vision", "Computer Vision", "Computer vision and image processing"),
        ("data-science", "Data Science", "Data science and analytics"),
        ("neural-networks", "Neural Networks", "Neural network architectures"),
        ("transformers", "Transformers", "Transformer models"),
        ("llm", "Large Language Models", "Large language models"),
        ("gpt", "GPT", "GPT models and variants"),
        ("bert", "BERT", "BERT and variants"),
        ("reinforcement-learning", "Reinforcement Learning", "RL algorithms"),
        ("supervised-learning", "Supervised Learning", "Supervised ML methods"),
        ("unsupervised-learning", "Unsupervised Learning", "Unsupervised ML methods"),
        ("classification", "Classification", "Classification algorithms"),
        ("regression", "Regression", "Regression analysis"),
        ("clustering", "Clustering", "Clustering algorithms"),
        ("recommendation-systems", "Recommendation Systems", "Recommendation engines"),
        ("time-series", "Time Series", "Time series analysis"),
        ("anomaly-detection", "Anomaly Detection", "Anomaly detection methods"),
        ("feature-engineering", "Feature Engineering", "Feature selection and engineering"),
        ("model-deployment", "Model Deployment", "ML model deployment"),
        ("mlops", "MLOps", "ML operations and lifecycle"),
        ("automl", "AutoML", "Automated machine learning"),
        ("explainable-ai", "Explainable AI", "AI interpretability"),
        ("ai-ethics", "AI Ethics", "AI ethics and fairness")
    ]
    
    # Domain-Specific (30 tags)
    domains = [
        ("healthcare", "Healthcare", "Healthcare and medical applications"),
        ("fintech", "FinTech", "Financial technology"),
        ("ecommerce", "E-commerce", "Electronic commerce"),
        ("education", "Education", "Educational technology"),
        ("gaming", "Gaming", "Game development and gaming"),
        ("iot", "Internet of Things", "IoT devices and systems"),
        ("blockchain", "Blockchain", "Blockchain technology"),
        ("cryptocurrency", "Cryptocurrency", "Digital currencies"),
        ("cybersecurity", "Cybersecurity", "Security and protection"),
        ("devops", "DevOps", "Development operations"),
        ("mobile-development", "Mobile Development", "Mobile app development"),
        ("web-development", "Web Development", "Web application development"),
        ("api-development", "API Development", "API design and development"),
        ("database-design", "Database Design", "Database architecture"),
        ("ui-ux", "UI/UX Design", "User interface and experience"),
        ("product-management", "Product Management", "Product strategy and management"),
        ("project-management", "Project Management", "Project planning and execution"),
        ("agile", "Agile", "Agile development methodologies"),
        ("scrum", "Scrum", "Scrum framework"),
        ("kanban", "Kanban", "Kanban methodology"),
        ("testing", "Software Testing", "Testing and quality assurance"),
        ("performance-optimization", "Performance Optimization", "System performance tuning"),
        ("scalability", "Scalability", "System scalability design"),
        ("monitoring", "System Monitoring", "Monitoring and observability"),
        ("logging", "Logging", "Application logging"),
        ("debugging", "Debugging", "Code debugging and troubleshooting"),
        ("code-review", "Code Review", "Code review processes"),
        ("documentation", "Documentation", "Technical documentation"),
        ("version-control", "Version Control", "Git and version control"),
        ("open-source", "Open Source", "Open source development")
    ]
    
    # Business & Professional (20 tags)
    business = [
        ("business-analysis", "Business Analysis", "Business requirements analysis"),
        ("data-analytics", "Data Analytics", "Business data analytics"),
        ("reporting", "Business Reporting", "Report generation and BI"),
        ("crm", "Customer Relationship Management", "CRM systems"),
        ("erp", "Enterprise Resource Planning", "ERP systems"),
        ("marketing", "Digital Marketing", "Marketing strategies"),
        ("seo", "Search Engine Optimization", "SEO optimization"),
        ("content-marketing", "Content Marketing", "Content strategy"),
        ("social-media", "Social Media", "Social media management"),
        ("email-marketing", "Email Marketing", "Email campaigns"),
        ("sales", "Sales", "Sales processes and automation"),
        ("customer-support", "Customer Support", "Customer service tools"),
        ("hr", "Human Resources", "HR management systems"),
        ("accounting", "Accounting", "Financial accounting"),
        ("legal", "Legal", "Legal technology and compliance"),
        ("compliance", "Regulatory Compliance", "Compliance management"),
        ("risk-management", "Risk Management", "Risk assessment"),
        ("supply-chain", "Supply Chain", "Supply chain management"),
        ("logistics", "Logistics", "Logistics and shipping"),
        ("consulting", "Business Consulting", "Consulting services")
    ]
    
    # Health & Accessibility (15 tags)
    health = [
        ("mental-health", "Mental Health", "Mental health and wellness"),
        ("adhd", "ADHD", "ADHD support and tools"),
        ("autism", "Autism", "Autism support and tools"),
        ("accessibility", "Accessibility", "Digital accessibility"),
        ("assistive-technology", "Assistive Technology", "AT for disabilities"),
        ("telemedicine", "Telemedicine", "Remote healthcare"),
        ("medical-imaging", "Medical Imaging", "Medical image analysis"),
        ("clinical-trials", "Clinical Trials", "Clinical research"),
        ("pharmacy", "Pharmacy", "Pharmaceutical systems"),
        ("fitness", "Fitness", "Health and fitness tracking"),
        ("nutrition", "Nutrition", "Nutritional analysis"),
        ("wellness", "Wellness", "Wellness and lifestyle"),
        ("therapy", "Therapy", "Therapeutic applications"),
        ("rehabilitation", "Rehabilitation", "Rehabilitation technology"),
        ("elderly-care", "Elderly Care", "Senior care technology")
    ]
    
    # Creative & Media (15 tags)
    creative = [
        ("content-creation", "Content Creation", "Digital content creation"),
        ("video-editing", "Video Editing", "Video production and editing"),
        ("audio-processing", "Audio Processing", "Audio editing and processing"),
        ("graphic-design", "Graphic Design", "Visual design and graphics"),
        ("photography", "Photography", "Photography and image editing"),
        ("animation", "Animation", "Animation and motion graphics"),
        ("3d-modeling", "3D Modeling", "3D design and modeling"),
        ("game-design", "Game Design", "Video game design"),
        ("storytelling", "Storytelling", "Narrative and story creation"),
        ("writing", "Creative Writing", "Writing and authoring"),
        ("journalism", "Journalism", "News and journalism"),
        ("publishing", "Publishing", "Digital publishing"),
        ("podcasting", "Podcasting", "Podcast production"),
        ("streaming", "Live Streaming", "Live streaming technology"),
        ("virtual-reality", "Virtual Reality", "VR applications")
    ]
    
    # Specialized Tools & Platforms (20 tags)
    tools = [
        ("automation-tools", "Automation Tools", "Process automation platforms"),
        ("workflow-management", "Workflow Management", "Workflow orchestration"),
        ("collaboration", "Team Collaboration", "Collaboration platforms"),
        ("communication", "Communication", "Communication tools"),
        ("file-management", "File Management", "File organization systems"),
        ("backup-recovery", "Backup & Recovery", "Data backup solutions"),
        ("virtualization", "Virtualization", "Virtual machines and containers"),
        ("network-administration", "Network Administration", "Network management"),
        ("system-administration", "System Administration", "System admin tools"),
        ("server-management", "Server Management", "Server administration"),
        ("cloud-migration", "Cloud Migration", "Cloud migration strategies"),
        ("disaster-recovery", "Disaster Recovery", "DR planning and execution"),
        ("capacity-planning", "Capacity Planning", "Resource capacity planning"),
        ("cost-optimization", "Cost Optimization", "Cost management and optimization"),
        ("vendor-management", "Vendor Management", "Vendor relationship management"),
        ("asset-management", "Asset Management", "IT asset management"),
        ("change-management", "Change Management", "Change control processes"),
        ("incident-management", "Incident Management", "Incident response"),
        ("knowledge-management", "Knowledge Management", "Knowledge base systems"),
        ("training", "Training & Development", "Learning and development")
    ]
    
    # Combine all categories
    all_categories = [
        languages, frameworks, cloud, ai_ml, domains, 
        business, health, creative, tools
    ]
    
    # Build final tag list
    for category in all_categories:
        for tag_id, name, description in category:
            tags.append({
                "id": tag_id,
                "name": name,
                "description": description
            })
    
    # Add some general utility tags
    utility_tags = [
        ("productivity", "Productivity", "Productivity enhancement"),
        ("organization", "Organization", "Task and time organization"),
        ("research", "Research", "Research and information gathering"),
        ("analysis", "Analysis", "Data and information analysis"),
        ("visualization", "Data Visualization", "Data visualization and charts"),
        ("reporting", "Reporting", "Report generation"),
        ("dashboard", "Dashboard", "Dashboard creation"),
        ("integration", "System Integration", "System integration"),
        ("migration", "Data Migration", "Data migration tools"),
        ("optimization", "Optimization", "Performance optimization")
    ]
    
    for tag_id, name, description in utility_tags:
        tags.append({
            "id": tag_id,
            "name": name,
            "description": description
        })
    
    return {"tags": tags}

def main():
    """Generate and save comprehensive tags"""
    tags_data = generate_comprehensive_tags()
    
    # Save to file
    output_path = Path("ai-agent/taxonomies/tags.json")
    with open(output_path, 'w') as f:
        json.dump(tags_data, f, indent=2)
    
    print(f"✅ Generated {len(tags_data['tags'])} comprehensive tags")
    print(f"📄 Saved to: {output_path}")
    
    # Show some examples
    print("\n🏷️ Sample tags:")
    for i, tag in enumerate(tags_data['tags'][:10]):
        print(f"   {tag['id']}: {tag['name']} - {tag['description']}")
    print(f"   ... and {len(tags_data['tags']) - 10} more")

if __name__ == "__main__":
    main()
