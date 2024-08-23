// For more information, see https://crawlee.dev/
/*import { PlaywrightCrawler} from 'crawlee';

// PlaywrightCrawler crawls the web using a headless
// browser controlled by the Playwright library.*/

import { PlaywrightCrawler, Dataset } from 'crawlee';

const momoCrawler = new PlaywrightCrawler({
    async requestHandler({ page, pushData }) {
        // Wait for the elements to be present
        await page.waitForSelector('div.swiper-slide.swiper-slide-next>img');
        await page.waitForSelector('h3.prdName');

        // Use locator to target multiple elements
        const imgLocators = page.locator('div.swiper-slide.swiper-slide-next>img');
        const nameLocators = page.locator('h3.prdName');

        // Extract src attributes from images
        const imgsrc = await imgLocators.evaluateAll(imgs => imgs.map(img => img.getAttribute('src')));

        // Extract text content from product names
        const prodnames = await nameLocators.allTextContents();

        // Use regex to extract brands from product names
        const regexselect = /[【\[](.+?)[】\]]/;
        const brands = prodnames.map(name => {
            const match = name.match(regexselect);
            return match ? match[1] : null;
        });

        // Push the data to the dataset
        /*await Dataset.pushData({
            brand: brands,
            image: imgsrc,
            product_name: prodnames,
        });*/
        
        // Push each product data entry as a separate row
        for (let i = 0; i < prodnames.length; i++) {
            await pushData({
                brand: brands[i],  // Single value for the brand
                image: imgsrc[i],  // Single value for the image
                product_name: prodnames[i]  // Single value for the product name
            });
        }
        //await Dataset.exportToCSV('results')
    },
    maxRequestsPerCrawl: 20,
    //headless: false,
});

await momoCrawler.run([
    'https://www.momoshop.com.tw/search/searchShop.jsp?keyword=Nike&searchType=1&curPage=1&_isFuzzy=0&showType=chessboardType&isBrandCategory=N&serviceCode=MT01'
]);

const dataset = await Dataset.open();
await dataset.exportToCSV('results.csv');

