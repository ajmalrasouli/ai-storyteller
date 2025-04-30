import { initialize, App, ContextType, TabInstance } from '@microsoft/teams-js';

export class TeamsService {
    private app: App | null = null;
    private context: any = null;

    constructor() {
        this.initializeTeams();
    }

    private async initializeTeams() {
        try {
            await initialize();
            this.app = App();
            await this.getContext();
        } catch (error) {
            console.error('Failed to initialize Teams:', error);
        }
    }

    private async getContext() {
        try {
            this.context = await this.app.getContext();
            return this.context;
        } catch (error) {
            console.error('Failed to get Teams context:', error);
            return null;
        }
    }

    public async sendMessage(message: string) {
        try {
            if (!this.app) {
                await this.initializeTeams();
            }
            
            if (this.context && this.context.channelId) {
                // Send message to the channel
                // This would typically use your backend API
                // which would then use Microsoft Graph API
                console.log('Sending message to channel:', this.context.channelId);
            }
        } catch (error) {
            console.error('Failed to send message:', error);
        }
    }

    public async openTab(url: string) {
        try {
            if (!this.app) {
                await this.initializeTeams();
            }
            
            const tabInstance: TabInstance = {
                entityId: 'story-tab',
                contentUrl: url,
                suggestedDisplayName: 'AI Storyteller'
            };
            
            await this.app.openTab(tabInstance);
        } catch (error) {
            console.error('Failed to open tab:', error);
        }
    }

    public isInTeams(): boolean {
        return typeof window !== 'undefined' && window.microsoftTeams !== undefined;
    }

    public getTeamsContext(): any {
        return this.context;
    }
}
