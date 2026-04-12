export default {
    async fetch(request) {
        const url = new URL(request.url);
        const target = url.searchParams.get('url');

        if (!target || !target.startsWith('https://drive.google.com/')) {
            return new Response('Forbidden', { status: 403 });
        }

        try {
            const resp = await fetch(target, {
                headers: { 'User-Agent': 'Mozilla/5.0' },
                redirect: 'follow'
            });

            const data = await resp.arrayBuffer();
            return new Response(data, {
                headers: {
                    'Content-Type': resp.headers.get('Content-Type') || 'application/pdf',
                    'Access-Control-Allow-Origin': '*',
                    'Cache-Control': 'public, max-age=3600'
                }
            });
        } catch (e) {
            return new Response(e.message, { status: 502 });
        }
    }
};
