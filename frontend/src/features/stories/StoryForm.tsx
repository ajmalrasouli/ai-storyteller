import React, { useState } from 'react';
import { storyApi } from '../../services/api';
import { StoryFormData } from '../../types';

interface StoryFormProps {
    onSubmit: () => void;
}

export const StoryForm: React.FC<StoryFormProps> = ({ onSubmit }) => {
    const [formData, setFormData] = useState<StoryFormData>({
        title: '',
        theme: '',
        characters: [''],
        age_group: '5-8',
    });
    const [error, setError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setIsSubmitting(true);

        try {
            await storyApi.create({
                ...formData
            });
            onSubmit();
        } catch (err) {
            setError('Failed to create story. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleCharacterChange = (index: number, value: string) => {
        setFormData(prev => {
            const newCharacters = [...prev.characters];
            newCharacters[index] = value;
            return {
                ...prev,
                characters: newCharacters,
            };
        });
    };

    const addCharacter = () => {
        setFormData(prev => ({
            ...prev,
            characters: [...prev.characters, ''],
        }));
    };

    const removeCharacter = (index: number) => {
        setFormData(prev => ({
            ...prev,
            characters: prev.characters.filter((_, i) => i !== index),
        }));
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
                <div className="text-red-500 text-sm">
                    {error}
                </div>
            )}
            <div>
                <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                    Title
                </label>
                <input
                    type="text"
                    id="title"
                    name="title"
                    value={formData.title}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
            </div>
            <div>
                <label htmlFor="theme" className="block text-sm font-medium text-gray-700">
                    Theme
                </label>
                <input
                    type="text"
                    id="theme"
                    name="theme"
                    value={formData.theme}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
            </div>
            <div>
                <label className="block text-sm font-medium text-gray-700">
                    Characters
                </label>
                {formData.characters.map((character, index) => (
                    <div key={index} className="mt-1 flex space-x-2">
                        <input
                            type="text"
                            value={character}
                            onChange={(e) => handleCharacterChange(index, e.target.value)}
                            required
                            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                        />
                        <button
                            type="button"
                            onClick={() => removeCharacter(index)}
                            className="text-red-600 hover:text-red-800"
                        >
                            Remove
                        </button>
                    </div>
                ))}
                <button
                    type="button"
                    onClick={addCharacter}
                    className="mt-2 text-sm text-indigo-600 hover:text-indigo-800"
                >
                    Add Character
                </button>
            </div>
            <div>
                <label htmlFor="age_group" className="block text-sm font-medium text-gray-700">
                    Age Group
                </label>
                <select
                    id="age_group"
                    name="age_group"
                    value={formData.age_group}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                >
                    <option value="5-8">5-8 years</option>
                    <option value="9-12">9-12 years</option>
                    <option value="13+">13+ years</option>
                </select>
            </div>
            <button
                type="submit"
                disabled={isSubmitting}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
                {isSubmitting ? 'Creating...' : 'Create Story'}
            </button>
        </form>
    );
}; 