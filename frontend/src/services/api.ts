import { VerificationResult, HealthStatus, EvidenceArticle } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export async function analyzeClaim(claim: string, maxArticles: number = 5): Promise<VerificationResult> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        claim: claim.trim(),
        max_articles: maxArticles,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const detail = errorData.detail || 'Failed to analyze claim.';
      
      if (response.status === 429 || detail.toLowerCase().includes('rate limit') || detail.includes('429')) {
        throw new Error('API Quota Exceeded — ClarifAI reached provider limit. Try again shortly.');
      }
      throw new Error(detail);
    }

    return response.json();
  } catch (err: any) {
    if (err.name === 'TypeError' && err.message.includes('fetch')) {
      throw new Error('ClarifAI backend is currently unavailable.');
    }
    throw err;
  }
}

export async function fetchLatestNews(): Promise<EvidenceArticle[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/news`);
    if (!response.ok) return [];
    const data = await response.json();
    return data.articles || [];
  } catch {
    return [];
  }
}

export async function fetchHealthStatus(): Promise<HealthStatus> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    if (!response.ok) {
      return { status: 'degraded' };
    }
    return response.json();
  } catch {
    return { status: 'unavailable' };
  }
}
