# 🚀 Deployment Guide

## Deployment Options

### Option 1: Streamlit Cloud (Easiest - Free)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/road-safety-rag.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `web_interface.py`
   - Click "Deploy"

3. **Note:** Streamlit Cloud doesn't support Ollama directly. You'll need to:
   - Use a cloud Ollama service, OR
   - Deploy Ollama separately and connect via API

### Option 2: Docker Deployment

#### Build and Run:
```bash
# Build the image
docker build -t road-safety-rag .

# Run the container
docker run -p 8501:8501 \
  -v $(pwd)/interventions.json:/app/interventions.json:ro \
  road-safety-rag
```

#### Using Docker Compose:
```bash
docker-compose up -d
```

Access at: http://localhost:8501

### Option 3: Local Server Deployment

#### Using systemd (Linux):

1. Create service file: `/etc/systemd/system/road-safety-rag.service`
```ini
[Unit]
Description=Road Safety RAG Streamlit App
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/road-safety-rag
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/streamlit run web_interface.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

2. Enable and start:
```bash
sudo systemctl enable road-safety-rag
sudo systemctl start road-safety-rag
```

### Option 4: Cloud Platforms

#### AWS EC2:
1. Launch EC2 instance (Ubuntu)
2. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip3 install -r requirements_complete.txt
   ```
3. Install Ollama:
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ollama pull llama3.2:3b
   ```
4. Run with screen/tmux:
   ```bash
   screen -S streamlit
   streamlit run web_interface.py --server.port=8501 --server.address=0.0.0.0
   ```

#### Google Cloud Platform:
1. Create VM instance
2. Install dependencies (same as AWS)
3. Configure firewall rules for port 8501
4. Deploy using same steps

#### Azure:
1. Create Azure VM
2. Follow same installation steps
3. Configure Network Security Group for port 8501

### Option 5: Railway/Render/Fly.io

#### Railway:
1. Connect GitHub repository
2. Set build command: `pip install -r requirements_complete.txt`
3. Set start command: `streamlit run web_interface.py --server.port=$PORT`
4. Add Ollama service or use external API

#### Render:
1. Create new Web Service
2. Connect repository
3. Build: `pip install -r requirements_complete.txt`
4. Start: `streamlit run web_interface.py --server.port=$PORT --server.address=0.0.0.0`

## Environment Variables

Create `.env` file:
```env
OLLAMA_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## Production Checklist

- [ ] Set up proper authentication (if needed)
- [ ] Configure HTTPS/SSL
- [ ] Set up monitoring/logging
- [ ] Configure backup for data
- [ ] Set up error tracking
- [ ] Configure rate limiting
- [ ] Set up CI/CD pipeline
- [ ] Document API endpoints (if any)
- [ ] Set up health checks
- [ ] Configure auto-scaling (if needed)

## Security Considerations

1. **Authentication:** Add Streamlit authentication
2. **HTTPS:** Use reverse proxy (nginx) with SSL
3. **Rate Limiting:** Implement to prevent abuse
4. **Input Validation:** Validate all user inputs
5. **Secrets Management:** Use environment variables for sensitive data

## Monitoring

### Health Check Endpoint:
- Streamlit: `http://your-domain:8501/_stcore/health`

### Logging:
- Application logs: Check Streamlit console output
- System logs: Check systemd/journalctl (Linux)

## Troubleshooting

### Port Already in Use:
```bash
# Find process using port 8501
lsof -i :8501
# Kill process
kill -9 <PID>
```

### Ollama Connection Issues:
- Ensure Ollama is running: `ollama list`
- Check Ollama URL in environment variables
- Verify firewall rules

### Memory Issues:
- Reduce `top_k` value
- Use smaller Ollama model
- Increase server RAM

## Performance Optimization

1. **Caching:** Already implemented with `@st.cache_resource`
2. **Embeddings:** Pre-compute and save embeddings
3. **Model Size:** Use smaller models for faster inference
4. **CDN:** Use CDN for static assets
5. **Load Balancing:** For high traffic

## Backup Strategy

1. **Data Backup:**
   ```bash
   # Backup interventions.json
   cp interventions.json backups/interventions_$(date +%Y%m%d).json
   
   # Backup embeddings
   cp road_safety_index.pkl backups/index_$(date +%Y%m%d).pkl
   ```

2. **Automated Backups:**
   - Set up cron job for daily backups
   - Use cloud storage (S3, GCS) for backups

## Support

For deployment issues:
1. Check logs: `docker logs road-safety-rag-app`
2. Verify dependencies: `python verify_setup.py`
3. Test locally before deploying
4. Check network connectivity

