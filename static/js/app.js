// 뉴스 소스별 로고 및 색상 설정
const NEWS_SOURCES = {
    '매일경제': {
        logo: 'https://img.mk.co.kr/main/2023/mk_logo.png',
        color: '#E8F3FF'
    },
    '네이버경제': {
        logo: 'https://ssl.pstatic.net/static/newsstand/2020/logo/light/0000.png',
        color: '#E8FFE8'
    },
    '조선비즈': {
        logo: 'https://biz.chosun.com/static/img/common/chosunbiz_logo.png',
        color: '#FFE8E8'
    },
    '연합뉴스': {
        logo: 'https://www.yna.co.kr/static/img/common/yna_logo.png',
        color: '#F0E8FF'
    },
    '아시아경제': {
        logo: 'https://www.asiae.co.kr/resources/images/common/asiae-logo.png',
        color: '#FFE8F0'
    },
    'Reuters': {
        logo: 'https://www.reuters.com/pf/resources/images/reuters/logo-vertical-default.svg?d=165',
        color: '#E8F0FF'
    },
    'MarketWatch': {
        logo: 'https://mw3.wsj.net/mw5/content/logos/mw_logo_social.png',
        color: '#FFF0E8'
    },
    'CNBC': {
        logo: 'https://www.cnbc.com/static/img/cnbc-logo.png',
        color: '#E8FFF0'
    }
};

// 현재 시간 업데이트 함수
function updateCurrentTime() {
    const options = {
        timeZone: 'Asia/Seoul',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    };
    const now = new Date();
    document.getElementById('current-time').textContent = 
        now.toLocaleString('ko-KR', options) + ' KST';
}

// 뉴스 카드 생성 함수
function createNewsCard(source, articles) {
    const card = document.createElement('div');
    card.className = 'news-card';
    card.style.backgroundColor = NEWS_SOURCES[source]?.color || '#ffffff';

    const sourceDiv = document.createElement('div');
    sourceDiv.className = 'news-source';
    sourceDiv.innerHTML = `
        <img src="${NEWS_SOURCES[source]?.logo || ''}" alt="${source} 로고">
        <h3>${source}</h3>
    `;

    const newsList = document.createElement('ul');
    newsList.className = 'news-list';

    articles.forEach((article, index) => {
        const li = document.createElement('li');
        li.className = 'news-item';
        
        const viewCount = article.views 
            ? `<span class="view-count">👁️ ${article.views}</span>`
            : '';

        li.innerHTML = `
            <a href="${article.link}" target="_blank">${article.title}</a>
            ${viewCount}
        `;

        newsList.appendChild(li);
    });

    card.appendChild(sourceDiv);
    card.appendChild(newsList);
    return card;
}

// 뉴스 데이터 가져오기
async function fetchNews() {
    try {
        const response = await fetch('/api/news');
        const data = await response.json();

        // 수집 시간 업데이트
        document.getElementById('collected-time').textContent = data.timestamp;

        // 국내 뉴스 렌더링
        const domesticGrid = document.getElementById('domestic-grid');
        domesticGrid.innerHTML = '';
        data.domestic.forEach(article => {
            const card = createNewsCard(article.source, [article]);
            domesticGrid.appendChild(card);
        });

        // 해외 뉴스 렌더링
        const internationalGrid = document.getElementById('international-grid');
        internationalGrid.innerHTML = '';
        data.international.forEach(article => {
            const card = createNewsCard(article.source, [article]);
            internationalGrid.appendChild(card);
        });

    } catch (error) {
        console.error('뉴스를 가져오는 중 오류가 발생했습니다:', error);
    }
}

// 이벤트 리스너 설정
document.addEventListener('DOMContentLoaded', () => {
    // 초기 로드
    fetchNews();
    updateCurrentTime();

    // 시계 업데이트
    setInterval(updateCurrentTime, 1000);

    // 새로고침 버튼
    document.getElementById('refresh-btn').addEventListener('click', fetchNews);
}); 