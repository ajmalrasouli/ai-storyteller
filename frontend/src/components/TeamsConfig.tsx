import React, { useState } from 'react';
import { initialize, App, ContextType } from '@microsoft/teams-js';

const TeamsConfig: React.FC = () => {
    const [configurationComplete, setConfigurationComplete] = useState(false);
    const [error, setError] = useState<string | null>(null);

    React.useEffect(() => {
        const initializeTeams = async () => {
            try {
                await initialize();
                const app = App();
                const context = await app.getContext();

                if (context.app.type === ContextType.Tab) {
                    // Handle tab configuration
                    const tabInstance = {
                        entityId: 'story-tab',
                        contentUrl: 'https://proud-water-076db370f.6.azurestaticapps.net',
                        suggestedDisplayName: 'AI Storyteller'
                    };

                    await app.submitTabConfiguration(tabInstance);
                    setConfigurationComplete(true);
                }
            } catch (err) {
                setError(err.message);
            }
        };

        initializeTeams();
    }, []);

    if (configurationComplete) {
        return (
            <div>
                <h1>Configuration Complete</h1>
                <p>Your tab has been configured successfully!</p>
            </div>
        );
    }

    if (error) {
        return (
            <div>
                <h1>Error</h1>
                <p>{error}</p>
            </div>
        );
    }

    return (
        <div>
            <h1>AI Storyteller Teams Configuration</h1>
            <p>Configuring your Teams tab...</p>
        </div>
    );
};

export default TeamsConfig;
