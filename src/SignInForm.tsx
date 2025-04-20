"use client";
import { useState } from "react";
import { login, register } from "./lib/api";
import { toast } from "react-hot-toast";

interface SignInFormProps {
  onSignIn: (token: string) => void;
}

export default function SignInForm({ onSignIn }: SignInFormProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isRegistering, setIsRegistering] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      if (isRegistering) {
        await register(email, password);
        toast.success("Account created successfully! Please sign in.");
        setIsRegistering(false);
      } else {
        const response = await login(email, password);
        onSignIn(response.token);
        toast.success("Signed in successfully!");
      }
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-center">
        {isRegistering ? "Create Account" : "Sign In"}
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">
            Email
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            required
          />
        </div>
        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700">
            Password
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            required
          />
        </div>
        <button
          type="submit"
          disabled={isLoading}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {isLoading ? "Loading..." : isRegistering ? "Register" : "Sign In"}
        </button>
      </form>
      <button
        type="button"
        onClick={() => setIsRegistering(!isRegistering)}
        className="w-full text-sm text-indigo-600 hover:text-indigo-500"
      >
        {isRegistering ? "Already have an account? Sign in" : "Don't have an account? Register"}
      </button>
    </div>
  );
}
