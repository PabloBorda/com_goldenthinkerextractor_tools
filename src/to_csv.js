const fs = require('fs');
const axios = require('axios');
const csv = require('csv-parser');

async function searchContactInfo(name, company) {
    const query = `${name} ${company} email OR phone`;
    const url = `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json`;

    try {
        const response = await axios.get(url);
        const data = response.data;

        let email = null;
        let phone = null;

        if (data.Results) {
            for (const result of data.Results) {
                if (result.FirstURL) {
                    const resultUrl = result.FirstURL;
                    if (resultUrl.includes('mailto:')) {
                        email = resultUrl.split('mailto:')[1].split('?')[0];
                    } else if (resultUrl.includes('tel:')) {
                        phone = resultUrl.split('tel:')[1].split('?')[0];
                    }
                }
            }
        }

        return { email, phone };
    } catch (error) {
        console.error(`Error searching contact info for ${name} at ${company}:`, error.message);
        return { email: null, phone: null };
    }
}

async function generateContacts(inputCsvPath, outputCsvPath) {
    console.log(`Starting CSV processing for input file: ${inputCsvPath}`);

    const writeStream = fs.createWriteStream(outputCsvPath);

    writeStream.write('name,company,email,phone\n');

    fs.createReadStream(inputCsvPath)
        .pipe(csv())
        .on('data', async (row) => {
            if (row && row.name && row.company) {
                const name = row.name.trim();
                const company = row.company.trim();

                console.log(`Searching contact info for ${name} at ${company}...`);

                const { email, phone } = await searchContactInfo(name, company);

                const csvRow = `${name},${company},${email || ''},${phone || ''}\n`;
                writeStream.write(csvRow);

                console.log(`Contact info found for ${name} at ${company}: Email=${email || 'N/A'}, Phone=${phone || 'N/A'}`);
            } else {
                console.warn('Skipping invalid row:', row);
            }
        })
        .on('end', () => {
            writeStream.end();
            console.log(`CSV processing completed. Output file: ${outputCsvPath}`);
        })
        .on('error', (error) => {
            console.error('Error reading input CSV:', error.message);
        });
}

const inputCsvFile = process.argv[2];
const outputCsvFile = process.argv[3];

if (!inputCsvFile || !outputCsvFile) {
    console.error('Usage: node to_csv.js <inputCsvFile> <outputCsvFile>');
    process.exit(1);
}

generateContacts(inputCsvFile, outputCsvFile);
