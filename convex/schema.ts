import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";
import { authTables } from "@convex-dev/auth/server";

const applicationTables = {
  stories: defineTable({
    title: v.string(),
    content: v.string(),
    theme: v.string(),
    characters: v.array(v.string()),
    ageGroup: v.string(),
    authorId: v.string(),
    isFavorite: v.boolean(),
  }).index("by_author", ["authorId"]),
};

export default defineSchema({
  ...authTables,
  ...applicationTables,
});
