const { TestAdapter, ActivityTypes } = require('botbuilder');
const { TeamsBotService } = require('../backend/services/teams_bot_service');
const logger = require('../backend/config/logger');

describe('Teams Bot Tests', () => {
    let storage = {};
    let adapter;
    let bot;

    beforeEach(() => {
        adapter = new TestAdapter();
        bot = new TeamsBotService();
    });

    test('Bot responds to message', async () => {
        const testMessage = 'Hello bot';
        
        await adapter.test(testMessage, async (context) => {
            try {
                await bot.run(context);
                logger.info('Bot responded successfully');
            } catch (error) {
                logger.error('Bot failed to respond', { error: error.message });
                throw error;
            }
        });
    });
});