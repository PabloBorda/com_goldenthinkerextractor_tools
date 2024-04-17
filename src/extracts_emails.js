const axios = require('axios');

async function searchDuckDuckGo(query) {
    try {
        const response = await axios.get('https://api.duckduckgo.com', {
            params: {
                q: query,
                format: 'json',
                t: 'nodejs'
            }
        });

        if (response.status === 200) {
            const data = response.data;
            console.log('API Response:', data); // Log the full API response

            if (data.AbstractText) {
                return data.AbstractText;
            } else if (data.RelatedTopics && data.RelatedTopics.length > 0 && data.RelatedTopics[0].Text) {
                return data.RelatedTopics[0].Text;
            } else {
                // Log a warning if no relevant information was found
                console.warn('No relevant information found in response:', data);
                return 'No relevant information found.';
            }
        } else {
            throw new Error('Failed to fetch data');
        }
    } catch (error) {
        console.error('Error fetching data:', error.message);
        return 'Error fetching search results';
    }
}

// Example usage:
const searchQuery = 'Your Search Query Here';
searchDuckDuckGo(searchQuery)
    .then(result => {
        console.log('Search Results:', result);
    })
    .catch(err => {
        console.error('Search Error:', err);
    });
