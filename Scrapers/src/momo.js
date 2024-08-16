// For more information, see https://crawlee.dev/
import { PlaywrightCrawler } from 'crawlee';

// PlaywrightCrawler crawls the web using a headless
// browser controlled by the Playwright library.
const momoCrawler = new PlaywrightCrawler({
    // Use the requestHandler to process each of the crawled pages.
    async requestHandler({ request, page, enqueueLinks, log, pushData }) {
        await page.waitForSelector('div.swiper-slide.swiper-slide-next>img');

        const regexselect = /[【\[](.+?)[】\]]/
    
        var imgs = Array.from(page.locator("div.swiper-slide.swiper-slide-next>img"));
        var imgsrc = imgs.map(img => img.getAttribute("src"));
    
        await page.waitForSelector('h3.prdName');
    
        var names = Array.from(page.locator("h3.prdName"));
        var prodnames = names.map(name => name.textContent());
        
        // Stuff for momo b/c they just put the brand in brackets at the front
        var brands = prodnames.map(matches => {
            const match = matches.match(regexselect); // Get the first match only
            return match ? match[1] : null; // Return the captured group, or null if no match
        });
        
        // Return an object with the data extracted from the page.
        // It will be stored to the resulting dataset.
        await pushData({
            brand: brands,
            image: imgsrc,
            product_name: prodnames,
        });
    },
    // Comment this option to scrape the full website.
    maxRequestsPerCrawl: 20,
    // Uncomment this option to see the browser window.
    headless: false,
});

// Add first URL to the queue and start the crawl.
await momoCrawler.run([
    'https://www.momoshop.com.tw/search/searchShop.jsp?keyword=Nike&searchType=1&curPage=1&_isFuzzy=0&showType=chessboardType&isBrandCategory=N&serviceCode=MT01'
]);
