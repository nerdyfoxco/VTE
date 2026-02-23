export const UMP_RESPONSE_SCHEMA = {
    type: "json_schema",
    json_schema: {
        name: "ump_changeset",
        schema: {
            type: "object",
            properties: {
                edits: {
                    type: "array",
                    items: {
                        type: "object",
                        properties: {
                            path: {
                                type: "string",
                                description: "Relative file path (e.g., 'foundation/contracts/pipe-envelope.schema.json'). MUST be precisely listed in the UMP 'Files:' section."
                            },
                            content: {
                                type: "string",
                                description: "The full UTF-8 source code for the file, implementing the UMP constraint. Must be a complete file. Do not truncate."
                            }
                        },
                        required: ["path", "content"],
                        additionalProperties: false
                    }
                }
            },
            required: ["edits"],
            additionalProperties: false
        },
        strict: true
    }
};
