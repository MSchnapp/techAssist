const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const toolSchema = new Schema(
    {
        toolName: {type: String, index: "text"},
        roNumber: Number,
        scancurrent: Boolean,
        error: Boolean,
        prescan: Boolean,
        postscan: Boolean,
        paired: Boolean,
    },
    {timestamps: true}
);

module.exports = mongoose.model('Tools', toolSchema);