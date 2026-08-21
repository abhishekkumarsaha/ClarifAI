import {
  VerificationResult,
  HealthStatus,
  EvidenceArticle,
} from '../types';

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || '';

const NEWS_CACHE_KEY = 'clarifai_cached_news_v2';
const ONE_HOUR_MS = 60 * 60 * 1000;

// ============================================================
// RESPONSE PARSER
// ============================================================

async function parseResponse(response: Response): Promise<any> {
  const contentType =
    response.headers.get('content-type') || '';

  if (contentType.includes('application/json')) {
    return await response.json();
  }

  const text = await response.text();

  return {
    detail: text || 'Unknown backend error.',
  };
}

// ============================================================
// NORMALIZE EVIDENCE
// ============================================================

function normalizeEvidence(
  items: any,
): EvidenceArticle[] {
  if (!Array.isArray(items)) {
    return [];
  }

  return items.map((item: any) => ({
    publisher:
      item?.publisher ||
      item?.source ||
      item?.source_domain ||
      'Unknown Source',

    source_domain:
      item?.source_domain ||
      item?.source ||
      '',

    headline:
      item?.headline ||
      item?.title ||
      item?.article_title ||
      '',

    title:
      item?.title ||
      item?.headline ||
      item?.article_title ||
      '',

    publication_date:
      item?.publication_date ||
      item?.published_at ||
      '',

    finding:
      item?.finding ||
      item?.summary ||
      '',

    snippet:
      item?.snippet ||
      item?.description ||
      '',

    summary:
      item?.summary ||
      item?.finding ||
      '',

    url:
      item?.url ||
      item?.final_url ||
      item?.original_url ||
      '',
  }));
}

// ============================================================
// NORMALIZE VERIFICATION RESULT
// ============================================================

function normalizeVerificationResult(
  data: any,
): VerificationResult {
  return {
    ...data,

    success:
      data?.success !== false,

    claim:
      data?.claim || '',

    verdict:
      data?.verdict || 'UNVERIFIED',

    confidence:
      typeof data?.confidence === 'number'
        ? data.confidence
        : Number(data?.confidence || 0),

    confidence_level:
      data?.confidence_level ||
      'Very Low',

    summary:
      data?.summary ||
      'No verification summary available.',

    why:
      Array.isArray(data?.why)
        ? data.why
        : [],

    supporting_evidence:
      normalizeEvidence(
        data?.supporting_evidence,
      ),

    contradicting_evidence:
      normalizeEvidence(
        data?.contradicting_evidence,
      ),

    source_assessment:
      data?.source_assessment || '',

    ml_interpretation:
      data?.ml_interpretation || '',

    ml_results:
      Array.isArray(data?.ml_results)
        ? data.ml_results
        : [],

    limitations:
      Array.isArray(data?.limitations)
        ? data.limitations
        : [],

    user_safety:
      data?.user_safety || '',

    articles_found:
      Number(data?.articles_found || 0),

    timestamp:
      data?.timestamp ||
      new Date().toISOString(),

    error:
      data?.error,
  };
}

// ============================================================
// VERIFY / ANALYZE
// ============================================================

export async function analyzeClaim(
  claim: string,
  maxArticles: number = 5,
): Promise<VerificationResult> {

  const cleanedClaim = claim.trim();

  if (!cleanedClaim) {
    throw new Error(
      'Please enter a news claim or article URL.',
    );
  }

  try {

    const response = await fetch(
      `${API_BASE_URL}/api/analyze`,
      {
        method: 'POST',

        headers: {
          'Content-Type':
            'application/json',

          'Accept':
            'application/json',
        },

        body: JSON.stringify({
          claim: cleanedClaim,
          max_articles: maxArticles,
        }),
      },
    );

    const data =
      await parseResponse(response);

    if (!response.ok) {

      const detail =
        data?.detail ||
        data?.message ||
        'Failed to analyze the claim.';

      if (
        response.status === 429 ||
        String(detail)
          .toLowerCase()
          .includes('rate limit')
      ) {
        throw new Error(
          'API rate limit reached. Please try again shortly.',
        );
      }

      throw new Error(
        String(detail),
      );
    }

    return normalizeVerificationResult(
      data,
    );

  } catch (error) {

    if (error instanceof Error) {

      if (
        error.message
          .toLowerCase()
          .includes('failed to fetch') ||

        error.message
          .toLowerCase()
          .includes('networkerror') ||

        error.message
          .toLowerCase()
          .includes('fetch')
      ) {

        throw new Error(
          'ClarifAI backend is currently unavailable.',
        );
      }

      throw error;
    }

    throw new Error(
      'Unable to connect to the ClarifAI backend.',
    );
  }
}

// ============================================================
// LATEST NEWS
// ============================================================

export async function fetchLatestNews(): Promise<
  EvidenceArticle[]
> {

  // ----------------------------------------------------------
  // CACHE
  // ----------------------------------------------------------

  try {

    const cachedStr =
      localStorage.getItem(
        NEWS_CACHE_KEY,
      );

    if (cachedStr) {

      const cachedData =
        JSON.parse(cachedStr);

      const now =
        Date.now();

      if (
        cachedData?.timestamp &&
        now - cachedData.timestamp <
        ONE_HOUR_MS &&
        Array.isArray(
          cachedData?.articles,
        ) &&
        cachedData.articles.length > 0
      ) {

        return normalizeEvidence(
          cachedData.articles,
        );
      }
    }

  } catch {
    // Ignore cache errors
  }

  // ----------------------------------------------------------
  // API
  // ----------------------------------------------------------

  try {

    const response =
      await fetch(
        `${API_BASE_URL}/api/news`,
        {
          method: 'GET',

          headers: {
            Accept:
              'application/json',
          },
        },
      );

    if (!response.ok) {
      return [];
    }

    const data =
      await response.json();

    let articles: any[] = [];

    if (Array.isArray(data)) {

      articles = data;

    } else if (
      Array.isArray(data?.articles)
    ) {

      articles =
        data.articles;
    }

    const normalized =
      normalizeEvidence(
        articles,
      );

    if (
      normalized.length > 0
    ) {

      try {

        localStorage.setItem(
          NEWS_CACHE_KEY,
          JSON.stringify({
            timestamp:
              Date.now(),

            articles:
              normalized,
          }),
        );

      } catch {
        // Ignore cache write errors
      }

      return normalized;
    }

    return [];

  } catch {
    return [];;
  }
}

// ============================================================
// FALLBACK NEWS
// ============================================================


// ============================================================
// HEALTH
// ============================================================

export async function fetchHealthStatus():
  Promise<HealthStatus> {

  try {

    const response =
      await fetch(
        `${API_BASE_URL}/health`,
        {
          method: 'GET',

          headers: {
            Accept:
              'application/json',
          },
        },
      );

    if (!response.ok) {

      return {
        status:
          'degraded',
      };
    }

    return await response.json();

  } catch {

    return {
      status:
        'unavailable',
    };
  }
}