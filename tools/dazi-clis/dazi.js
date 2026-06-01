#!/usr/bin/env node
"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __esm = (fn, res) => function __init() {
  return fn && (res = (0, fn[__getOwnPropNames(fn)[0]])(fn = 0)), res;
};
var __commonJS = (cb, mod) => function __require() {
  return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
};
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));

// node_modules/.pnpm/commander@12.1.0/node_modules/commander/lib/error.js
var require_error = __commonJS({
  "node_modules/.pnpm/commander@12.1.0/node_modules/commander/lib/error.js"(exports2) {
    var CommanderError2 = class extends Error {
      /**
       * Constructs the CommanderError class
       * @param {number} exitCode suggested exit code which could be used with process.exit
       * @param {string} code an id string representing the error
       * @param {string} message human-readable description of the error
       */
      constructor(exitCode, code, message) {
        super(message);
        Error.captureStackTrace(this, this.constructor);
        this.name = this.constructor.name;
        this.code = code;
        this.exitCode = exitCode;
        this.nestedError = void 0;
      }
    };
    var InvalidArgumentError2 = class extends CommanderError2 {
      /**
       * Constructs the InvalidArgumentError class
       * @param {string} [message] explanation of why argument is invalid
       */
      constructor(message) {
        super(1, "commander.invalidArgument", message);
        Error.captureStackTrace(this, this.constructor);
        this.name = this.constructor.name;
      }
    };
    exports2.CommanderError = CommanderError2;
    exports2.InvalidArgumentError = InvalidArgumentError2;
  }
});

// node_modules/.pnpm/commander@12.1.0/node_modules/commander/lib/argument.js
var require_argument = __commonJS({
  "node_modules/.pnpm/commander@12.1.0/node_modules/commander/lib/argument.js"(exports2) {
    var { InvalidArgumentError: InvalidArgumentError2 } = require_error();
    var Argument2 = class {
      /**
       * Initialize a new command argument with the given name and description.
       * The default is that the argument is required, and you can explicitly
       * indicate this with <> around the name. Put [] around the name for an optional argument.
       *
       * @param {string} name
       * @param {string} [description]
       */
      constructor(name, description) {
        this.description = description || "";
        this.variadic = false;
        this.parseArg = void 0;
        this.defaultValue = void 0;
        this.defaultValueDescription = void 0;
        this.argChoices = void 0;
        switch (name[0]) {
          case "<":
            this.required = true;
            this._name = name.slice(1, -1);
            break;
          case "[":
            this.required = false;
            this._name = name.slice(1, -1);
            break;
          default:
            this.required = true;
            this._name = name;
            break;
        }
        if (this._name.length > 3 && this._name.slice(-3) === "...") {
          this.variadic = true;
          this._name = this._name.slice(0, -3);
        }
      }
      /**
       * Return argument name.
       *
       * @return {string}
       */
      name() {
        return this._name;
      }
      /**
       * @package
       */
      _concatValue(value, previous) {
        if (previous === this.defaultValue || !Array.isArray(previous)) {
          return [value];
        }
        return previous.concat(value);
      }
      /**
       * Set the default value, and optionally supply the description to be displayed in the help.
       *
       * @param {*} value
       * @param {string} [description]
       * @return {Argument}
       */
      default(value, description) {
        this.defaultValue = value;
        this.defaultValueDescription = description;
        return this;
      }
      /**
       * Set the custom handler for processing CLI command arguments into argument values.
       *
       * @param {Function} [fn]
       * @return {Argument}
       */
      argParser(fn) {
        this.parseArg = fn;
        return this;
      }
      /**
       * Only allow argument value to be one of choices.
       *
       * @param {string[]} values
       * @return {Argument}
       */
      choices(values) {
        this.argChoices = values.slice();
        this.parseArg = (arg, previous) => {
          if (!this.argChoices.includes(arg)) {
            throw new InvalidArgumentError2(
              `Allowed choices are ${this.argChoices.join(", ")}.`
            );
          }
          if (this.variadic) {
            return this._concatValue(arg, previous);
          }
          return arg;
        };
        return this;
      }
      /**
       * Make argument required.
       *
       * @returns {Argument}
       */
      argRequired() {
        this.required = true;
        return this;
      }
      /**
       * Make argument optional.
       *
       * @returns {Argument}
       */
      argOptional() {
        this.required = false;
        return this;
      }
    };
    function humanReadableArgName(arg) {
      const nameOutput = arg.name() + (arg.variadic === true ? "..." : "");
      return arg.required ? "<" + nameOutput + ">" : "[" + nameOutput + "]";
    }
    exports2.Argument = Argument2;
    exports2.humanReadableArgName = humanReadableArgName;
  }
});

// node_modules/.pnpm/commander@12.1.0/node_modules/commander/lib/help.js
var require_help = __commonJS({
  "node_modules/.pnpm/commander@12.1.0/node_modules/commander/lib/help.js"(exports2) {
    var { humanReadableArgName } = require_argument();
    var Help2 = class {
      constructor() {
        this.helpWidth = void 0;
        this.sortSubcommands = false;
        this.sortOptions = false;
        this.showGlobalOptions = false;
      }
      /**
       * Get an array of the visible subcommands. Includes a placeholder for the implicit help command, if there is one.
       *
       * @param {Command} cmd
       * @returns {Command[]}
       */
      visibleCommands(cmd) {
        const visibleCommands = cmd.commands.filter((cmd2) => !cmd2._hidden);
        const helpCommand = cmd._getHelpCommand();
        if (helpCommand && !helpCommand._hidden) {
          visibleCommands.push(helpCommand);
        }
        if (this.sortSubcommands) {
          visibleCommands.sort((a, b) => {
            return a.name().localeCompare(b.name());
          });
        }
        return visibleCommands;
      }
      /**
       * Compare options for sort.
       *
       * @param {Option} a
       * @param {Option} b
       * @returns {number}
       */
      compareOptions(a, b) {
        const getSortKey = (option) => {
          return option.short ? option.short.replace(/^-/, "") : option.long.replace(/^--/, "");
        };
        return getSortKey(a).localeCompare(getSortKey(b));
      }
      /**
       * Get an array of the visible options. Includes a placeholder for the implicit help option, if there is one.
       *
       * @param {Command} cmd
       * @returns {Option[]}
       */
      visibleOptions(cmd) {
        const visibleOptions = cmd.options.filter((option) => !option.hidden);
        const helpOption = cmd._getHelpOption();
        if (helpOption && !helpOption.hidden) {
          const removeShort = helpOption.short && cmd._findOption(helpOption.short);
          const removeLong = helpOption.long && cmd._findOption(helpOption.long);
          if (!removeShort && !removeLong) {
            visibleOptions.push(helpOption);
          } else if (helpOption.long && !removeLong) {
            visibleOptions.push(
              cmd.createOption(helpOption.long, helpOption.description)
            );
          } else if (helpOption.short && !removeShort) {
            visibleOptions.push(
              cmd.createOption(helpOption.short, helpOption.description)
            );
          }
        }
        if (this.sortOptions) {
          visibleOptions.sort(this.compareOptions);
        }
        return visibleOptions;
      }
      /**
       * Get an array of the visible global options. (Not including help.)
       *
       * @param {Command} cmd
       * @returns {Option[]}
       */
      visibleGlobalOptions(cmd) {
        if (!this.showGlobalOptions) return [];
        const globalOptions = [];
        for (let ancestorCmd = cmd.parent; ancestorCmd; ancestorCmd = ancestorCmd.parent) {
          const visibleOptions = ancestorCmd.options.filter(
            (option) => !option.hidden
          );
          globalOptions.push(...visibleOptions);
        }
        if (this.sortOptions) {
          globalOptions.sort(this.compareOptions);
        }
        return globalOptions;
      }
      /**
       * Get an array of the arguments if any have a description.
       *
       * @param {Command} cmd
       * @returns {Argument[]}
       */
      visibleArguments(cmd) {
        if (cmd._argsDescription) {
          cmd.registeredArguments.forEach((argument) => {
            argument.description = argument.description || cmd._argsDescription[argument.name()] || "";
          });
        }
        if (cmd.registeredArguments.find((argument) => argument.description)) {
          return cmd.registeredArguments;
        }
        return [];
      }
      /**
       * Get the command term to show in the list of subcommands.
       *
       * @param {Command} cmd
       * @returns {string}
       */
      subcommandTerm(cmd) {
        const args = cmd.registeredArguments.map((arg) => humanReadableArgName(arg)).join(" ");
        return cmd._name + (cmd._aliases[0] ? "|" + cmd._aliases[0] : "") + (cmd.options.length ? " [options]" : "") + // simplistic check for non-help option
        (args ? " " + args : "");
      }
      /**
       * Get the option term to show in the list of options.
       *
       * @param {Option} option
       * @returns {string}
       */
      optionTerm(option) {
        return option.flags;
      }
      /**
       * Get the argument term to show in the list of arguments.
       *
       * @param {Argument} argument
       * @returns {string}
       */
      argumentTerm(argument) {
        return argument.name();
      }
      /**
       * Get the longest command term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestSubcommandTermLength(cmd, helper) {
        return helper.visibleCommands(cmd).reduce((max, command) => {
          return Math.max(max, helper.subcommandTerm(command).length);
        }, 0);
      }
      /**
       * Get the longest option term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestOptionTermLength(cmd, helper) {
        return helper.visibleOptions(cmd).reduce((max, option) => {
          return Math.max(max, helper.optionTerm(option).length);
        }, 0);
      }
      /**
       * Get the longest global option term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestGlobalOptionTermLength(cmd, helper) {
        return helper.visibleGlobalOptions(cmd).reduce((max, option) => {
          return Math.max(max, helper.optionTerm(option).length);
        }, 0);
      }
      /**
       * Get the longest argument term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestArgumentTermLength(cmd, helper) {
        return helper.visibleArguments(cmd).reduce((max, argument) => {
          return Math.max(max, helper.argumentTerm(argument).length);
        }, 0);
      }
      /**
       * Get the command usage to be displayed at the top of the built-in help.
       *
       * @param {Command} cmd
       * @returns {string}
       */
      commandUsage(cmd) {
        let cmdName = cmd._name;
        if (cmd._aliases[0]) {
          cmdName = cmdName + "|" + cmd._aliases[0];
        }
        let ancestorCmdNames = "";
        for (let ancestorCmd = cmd.parent; ancestorCmd; ancestorCmd = ancestorCmd.parent) {
          ancestorCmdNames = ancestorCmd.name() + " " + ancestorCmdNames;
        }
        return ancestorCmdNames + cmdName + " " + cmd.usage();
      }
      /**
       * Get the description for the command.
       *
       * @param {Command} cmd
       * @returns {string}
       */
      commandDescription(cmd) {
        return cmd.description();
      }
      /**
       * Get the subcommand summary to show in the list of subcommands.
       * (Fallback to description for backwards compatibility.)
       *
       * @param {Command} cmd
       * @returns {string}
       */
      subcommandDescription(cmd) {
        return cmd.summary() || cmd.description();
      }
      /**
       * Get the option description to show in the list of options.
       *
       * @param {Option} option
       * @return {string}
       */
      optionDescription(option) {
        const extraInfo = [];
        if (option.argChoices) {
          extraInfo.push(
            // use stringify to match the display of the default value
            `choices: ${option.argChoices.map((choice) => JSON.stringify(choice)).join(", ")}`
          );
        }
        if (option.defaultValue !== void 0) {
          const showDefault = option.required || option.optional || option.isBoolean() && typeof option.defaultValue === "boolean";
          if (showDefault) {
            extraInfo.push(
              `default: ${option.defaultValueDescription || JSON.stringify(option.defaultValue)}`
            );
          }
        }
        if (option.presetArg !== void 0 && option.optional) {
          extraInfo.push(`preset: ${JSON.stringify(option.presetArg)}`);
        }
        if (option.envVar !== void 0) {
          extraInfo.push(`env: ${option.envVar}`);
        }
        if (extraInfo.length > 0) {
          return `${option.description} (${extraInfo.join(", ")})`;
        }
        return option.description;
      }
      /**
       * Get the argument description to show in the list of arguments.
       *
       * @param {Argument} argument
       * @return {string}
       */
      argumentDescription(argument) {
        const extraInfo = [];
        if (argument.argChoices) {
          extraInfo.push(
            // use stringify to match the display of the default value
            `choices: ${argument.argChoices.map((choice) => JSON.stringify(choice)).join(", ")}`
          );
        }
        if (argument.defaultValue !== void 0) {
          extraInfo.push(
            `default: ${argument.defaultValueDescription || JSON.stringify(argument.defaultValue)}`
          );
        }
        if (extraInfo.length > 0) {
          const extraDescripton = `(${extraInfo.join(", ")})`;
          if (argument.description) {
            return `${argument.description} ${extraDescripton}`;
          }
          return extraDescripton;
        }
        return argument.description;
      }
      /**
       * Generate the built-in help text.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {string}
       */
      formatHelp(cmd, helper) {
        const termWidth = helper.padWidth(cmd, helper);
        const helpWidth = helper.helpWidth || 80;
        const itemIndentWidth = 2;
        const itemSeparatorWidth = 2;
        function formatItem(term, description) {
          if (description) {
            const fullText = `${term.padEnd(termWidth + itemSeparatorWidth)}${description}`;
            return helper.wrap(
              fullText,
              helpWidth - itemIndentWidth,
              termWidth + itemSeparatorWidth
            );
          }
          return term;
        }
        function formatList(textArray) {
          return textArray.join("\n").replace(/^/gm, " ".repeat(itemIndentWidth));
        }
        let output = [`Usage: ${helper.commandUsage(cmd)}`, ""];
        const commandDescription = helper.commandDescription(cmd);
        if (commandDescription.length > 0) {
          output = output.concat([
            helper.wrap(commandDescription, helpWidth, 0),
            ""
          ]);
        }
        const argumentList = helper.visibleArguments(cmd).map((argument) => {
          return formatItem(
            helper.argumentTerm(argument),
            helper.argumentDescription(argument)
          );
        });
        if (argumentList.length > 0) {
          output = output.concat(["Arguments:", formatList(argumentList), ""]);
        }
        const optionList = helper.visibleOptions(cmd).map((option) => {
          return formatItem(
            helper.optionTerm(option),
            helper.optionDescription(option)
          );
        });
        if (optionList.length > 0) {
          output = output.concat(["Options:", formatList(optionList), ""]);
        }
        if (this.showGlobalOptions) {
          const globalOptionList = helper.visibleGlobalOptions(cmd).map((option) => {
            return formatItem(
              helper.optionTerm(option),
              helper.optionDescription(option)
            );
          });
          if (globalOptionList.length > 0) {
            output = output.concat([
              "Global Options:",
              formatList(globalOptionList),
              ""
            ]);
          }
        }
        const commandList = helper.visibleCommands(cmd).map((cmd2) => {
          return formatItem(
            helper.subcommandTerm(cmd2),
            helper.subcommandDescription(cmd2)
          );
        });
        if (commandList.length > 0) {
          output = output.concat(["Commands:", formatList(commandList), ""]);
        }
        return output.join("\n");
      }
      /**
       * Calculate the pad width from the maximum term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      padWidth(cmd, helper) {
        return Math.max(
          helper.longestOptionTermLength(cmd, helper),
          helper.longestGlobalOptionTermLength(cmd, helper),
          helper.longestSubcommandTermLength(cmd, helper),
          helper.longestArgumentTermLength(cmd, helper)
        );
      }
      /**
       * Wrap the given string to width characters per line, with lines after the first indented.
       * Do not wrap if insufficient room for wrapping (minColumnWidth), or string is manually formatted.
       *
       * @param {string} str
       * @param {number} width
       * @param {number} indent
       * @param {number} [minColumnWidth=40]
       * @return {string}
       *
       */
      wrap(str, width, indent, minColumnWidth = 40) {
        const indents = " \\f\\t\\v\xA0\u1680\u2000-\u200A\u202F\u205F\u3000\uFEFF";
        const manualIndent = new RegExp(`[\\n][${indents}]+`);
        if (str.match(manualIndent)) return str;
        const columnWidth = width - indent;
        if (columnWidth < minColumnWidth) return str;
        const leadingStr = str.slice(0, indent);
        const columnText = str.slice(indent).replace("\r\n", "\n");
        const indentString = " ".repeat(indent);
        const zeroWidthSpace = "\u200B";
        const breaks = `\\s${zeroWidthSpace}`;
        const regex = new RegExp(
          `
|.{1,${columnWidth - 1}}([${breaks}]|$)|[^${breaks}]+?([${breaks}]|$)`,
          "g"
        );
        const lines = columnText.match(regex) || [];
        return leadingStr + lines.map((line, i) => {
          if (line === "\n") return "";
          return (i > 0 ? indentString : "") + line.trimEnd();
        }).join("\n");
      }
    };
    exports2.Help = Help2;
  }
});

// node_modules/.pnpm/commander@12.1.0/node_modules/commander/lib/option.js
var require_option = __commonJS({
  "node_modules/.pnpm/commander@12.1.0/node_modules/commander/lib/option.js"(exports2) {
    var { InvalidArgumentError: InvalidArgumentError2 } = require_error();
    var Option2 = class {
      /**
       * Initialize a new `Option` with the given `flags` and `description`.
       *
       * @param {string} flags
       * @param {string} [description]
       */
      constructor(flags, description) {
        this.flags = flags;
        this.description = description || "";
        this.required = flags.includes("<");
        this.optional = flags.includes("[");
        this.variadic = /\w\.\.\.[>\]]$/.test(flags);
        this.mandatory = false;
        const optionFlags = splitOptionFlags(flags);
        this.short = optionFlags.shortFlag;
        this.long = optionFlags.longFlag;
        this.negate = false;
        if (this.long) {
          this.negate = this.long.startsWith("--no-");
        }
        this.defaultValue = void 0;
        this.defaultValueDescription = void 0;
        this.presetArg = void 0;
        this.envVar = void 0;
        this.parseArg = void 0;
        this.hidden = false;
        this.argChoices = void 0;
        this.conflictsWith = [];
        this.implied = void 0;
      }
      /**
       * Set the default value, and optionally supply the description to be displayed in the help.
       *
       * @param {*} value
       * @param {string} [description]
       * @return {Option}
       */
      default(value, description) {
        this.defaultValue = value;
        this.defaultValueDescription = description;
        return this;
      }
      /**
       * Preset to use when option used without option-argument, especially optional but also boolean and negated.
       * The custom processing (parseArg) is called.
       *
       * @example
       * new Option('--color').default('GREYSCALE').preset('RGB');
       * new Option('--donate [amount]').preset('20').argParser(parseFloat);
       *
       * @param {*} arg
       * @return {Option}
       */
      preset(arg) {
        this.presetArg = arg;
        return this;
      }
      /**
       * Add option name(s) that conflict with this option.
       * An error will be displayed if conflicting options are found during parsing.
       *
       * @example
       * new Option('--rgb').conflicts('cmyk');
       * new Option('--js').conflicts(['ts', 'jsx']);
       *
       * @param {(string | string[])} names
       * @return {Option}
       */
      conflicts(names) {
        this.conflictsWith = this.conflictsWith.concat(names);
        return this;
      }
      /**
       * Specify implied option values for when this option is set and the implied options are not.
       *
       * The custom processing (parseArg) is not called on the implied values.
       *
       * @example
       * program
       *   .addOption(new Option('--log', 'write logging information to file'))
       *   .addOption(new Option('--trace', 'log extra details').implies({ log: 'trace.txt' }));
       *
       * @param {object} impliedOptionValues
       * @return {Option}
       */
      implies(impliedOptionValues) {
        let newImplied = impliedOptionValues;
        if (typeof impliedOptionValues === "string") {
          newImplied = { [impliedOptionValues]: true };
        }
        this.implied = Object.assign(this.implied || {}, newImplied);
        return this;
      }
      /**
       * Set environment variable to check for option value.
       *
       * An environment variable is only used if when processed the current option value is
       * undefined, or the source of the current value is 'default' or 'config' or 'env'.
       *
       * @param {string} name
       * @return {Option}
       */
      env(name) {
        this.envVar = name;
        return this;
      }
      /**
       * Set the custom handler for processing CLI option arguments into option values.
       *
       * @param {Function} [fn]
       * @return {Option}
       */
      argParser(fn) {
        this.parseArg = fn;
        return this;
      }
      /**
       * Whether the option is mandatory and must have a value after parsing.
       *
       * @param {boolean} [mandatory=true]
       * @return {Option}
       */
      makeOptionMandatory(mandatory = true) {
        this.mandatory = !!mandatory;
        return this;
      }
      /**
       * Hide option in help.
       *
       * @param {boolean} [hide=true]
       * @return {Option}
       */
      hideHelp(hide = true) {
        this.hidden = !!hide;
        return this;
      }
      /**
       * @package
       */
      _concatValue(value, previous) {
        if (previous === this.defaultValue || !Array.isArray(previous)) {
          return [value];
        }
        return previous.concat(value);
      }
      /**
       * Only allow option value to be one of choices.
       *
       * @param {string[]} values
       * @return {Option}
       */
      choices(values) {
        this.argChoices = values.slice();
        this.parseArg = (arg, previous) => {
          if (!this.argChoices.includes(arg)) {
            throw new InvalidArgumentError2(
              `Allowed choices are ${this.argChoices.join(", ")}.`
            );
          }
          if (this.variadic) {
            return this._concatValue(arg, previous);
          }
          return arg;
        };
        return this;
      }
      /**
       * Return option name.
       *
       * @return {string}
       */
      name() {
        if (this.long) {
          return this.long.replace(/^--/, "");
        }
        return this.short.replace(/^-/, "");
      }
      /**
       * Return option name, in a camelcase format that can be used
       * as a object attribute key.
       *
       * @return {string}
       */
      attributeName() {
        return camelcase(this.name().replace(/^no-/, ""));
      }
      /**
       * Check if `arg` matches the short or long flag.
       *
       * @param {string} arg
       * @return {boolean}
       * @package
       */
      is(arg) {
        return this.short === arg || this.long === arg;
      }
      /**
       * Return whether a boolean option.
       *
       * Options are one of boolean, negated, required argument, or optional argument.
       *
       * @return {boolean}
       * @package
       */
      isBoolean() {
        return !this.required && !this.optional && !this.negate;
      }
    };
    var DualOptions = class {
      /**
       * @param {Option[]} options
       */
      constructor(options) {
        this.positiveOptions = /* @__PURE__ */ new Map();
        this.negativeOptions = /* @__PURE__ */ new Map();
        this.dualOptions = /* @__PURE__ */ new Set();
        options.forEach((option) => {
          if (option.negate) {
            this.negativeOptions.set(option.attributeName(), option);
          } else {
            this.positiveOptions.set(option.attributeName(), option);
          }
        });
        this.negativeOptions.forEach((value, key) => {
          if (this.positiveOptions.has(key)) {
            this.dualOptions.add(key);
          }
        });
      }
      /**
       * Did the value come from the option, and not from possible matching dual option?
       *
       * @param {*} value
       * @param {Option} option
       * @returns {boolean}
       */
      valueFromOption(value, option) {
        const optionKey = option.attributeName();
        if (!this.dualOptions.has(optionKey)) return true;
        const preset = this.negativeOptions.get(optionKey).presetArg;
        const negativeValue = preset !== void 0 ? preset : false;
        return option.negate === (negativeValue === value);
      }
    };
    function camelcase(str) {
      return str.split("-").reduce((str2, word) => {
        return str2 + word[0].toUpperCase() + word.slice(1);
      });
    }
    function splitOptionFlags(flags) {
      let shortFlag;
      let longFlag;
      const flagParts = flags.split(/[ |,]+/);
      if (flagParts.length > 1 && !/^[[<]/.test(flagParts[1]))
        shortFlag = flagParts.shift();
      longFlag = flagParts.shift();
      if (!shortFlag && /^-[^-]$/.test(longFlag)) {
        shortFlag = longFlag;
        longFlag = void 0;
      }
      return { shortFlag, longFlag };
    }
    exports2.Option = Option2;
    exports2.DualOptions = DualOptions;
  }
});

// node_modules/.pnpm/commander@12.1.0/node_modules/commander/lib/suggestSimilar.js
var require_suggestSimilar = __commonJS({
  "node_modules/.pnpm/commander@12.1.0/node_modules/commander/lib/suggestSimilar.js"(exports2) {
    var maxDistance = 3;
    function editDistance(a, b) {
      if (Math.abs(a.length - b.length) > maxDistance)
        return Math.max(a.length, b.length);
      const d = [];
      for (let i = 0; i <= a.length; i++) {
        d[i] = [i];
      }
      for (let j = 0; j <= b.length; j++) {
        d[0][j] = j;
      }
      for (let j = 1; j <= b.length; j++) {
        for (let i = 1; i <= a.length; i++) {
          let cost = 1;
          if (a[i - 1] === b[j - 1]) {
            cost = 0;
          } else {
            cost = 1;
          }
          d[i][j] = Math.min(
            d[i - 1][j] + 1,
            // deletion
            d[i][j - 1] + 1,
            // insertion
            d[i - 1][j - 1] + cost
            // substitution
          );
          if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) {
            d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
          }
        }
      }
      return d[a.length][b.length];
    }
    function suggestSimilar(word, candidates) {
      if (!candidates || candidates.length === 0) return "";
      candidates = Array.from(new Set(candidates));
      const searchingOptions = word.startsWith("--");
      if (searchingOptions) {
        word = word.slice(2);
        candidates = candidates.map((candidate) => candidate.slice(2));
      }
      let similar = [];
      let bestDistance = maxDistance;
      const minSimilarity = 0.4;
      candidates.forEach((candidate) => {
        if (candidate.length <= 1) return;
        const distance = editDistance(word, candidate);
        const length = Math.max(word.length, candidate.length);
        const similarity = (length - distance) / length;
        if (similarity > minSimilarity) {
          if (distance < bestDistance) {
            bestDistance = distance;
            similar = [candidate];
          } else if (distance === bestDistance) {
            similar.push(candidate);
          }
        }
      });
      similar.sort((a, b) => a.localeCompare(b));
      if (searchingOptions) {
        similar = similar.map((candidate) => `--${candidate}`);
      }
      if (similar.length > 1) {
        return `
(Did you mean one of ${similar.join(", ")}?)`;
      }
      if (similar.length === 1) {
        return `
(Did you mean ${similar[0]}?)`;
      }
      return "";
    }
    exports2.suggestSimilar = suggestSimilar;
  }
});

// node_modules/.pnpm/commander@12.1.0/node_modules/commander/lib/command.js
var require_command = __commonJS({
  "node_modules/.pnpm/commander@12.1.0/node_modules/commander/lib/command.js"(exports2) {
    var EventEmitter = require("node:events").EventEmitter;
    var childProcess2 = require("node:child_process");
    var path13 = require("node:path");
    var fs16 = require("node:fs");
    var process8 = require("node:process");
    var { Argument: Argument2, humanReadableArgName } = require_argument();
    var { CommanderError: CommanderError2 } = require_error();
    var { Help: Help2 } = require_help();
    var { Option: Option2, DualOptions } = require_option();
    var { suggestSimilar } = require_suggestSimilar();
    var Command2 = class _Command extends EventEmitter {
      /**
       * Initialize a new `Command`.
       *
       * @param {string} [name]
       */
      constructor(name) {
        super();
        this.commands = [];
        this.options = [];
        this.parent = null;
        this._allowUnknownOption = false;
        this._allowExcessArguments = true;
        this.registeredArguments = [];
        this._args = this.registeredArguments;
        this.args = [];
        this.rawArgs = [];
        this.processedArgs = [];
        this._scriptPath = null;
        this._name = name || "";
        this._optionValues = {};
        this._optionValueSources = {};
        this._storeOptionsAsProperties = false;
        this._actionHandler = null;
        this._executableHandler = false;
        this._executableFile = null;
        this._executableDir = null;
        this._defaultCommandName = null;
        this._exitCallback = null;
        this._aliases = [];
        this._combineFlagAndOptionalValue = true;
        this._description = "";
        this._summary = "";
        this._argsDescription = void 0;
        this._enablePositionalOptions = false;
        this._passThroughOptions = false;
        this._lifeCycleHooks = {};
        this._showHelpAfterError = false;
        this._showSuggestionAfterError = true;
        this._outputConfiguration = {
          writeOut: (str) => process8.stdout.write(str),
          writeErr: (str) => process8.stderr.write(str),
          getOutHelpWidth: () => process8.stdout.isTTY ? process8.stdout.columns : void 0,
          getErrHelpWidth: () => process8.stderr.isTTY ? process8.stderr.columns : void 0,
          outputError: (str, write) => write(str)
        };
        this._hidden = false;
        this._helpOption = void 0;
        this._addImplicitHelpCommand = void 0;
        this._helpCommand = void 0;
        this._helpConfiguration = {};
      }
      /**
       * Copy settings that are useful to have in common across root command and subcommands.
       *
       * (Used internally when adding a command using `.command()` so subcommands inherit parent settings.)
       *
       * @param {Command} sourceCommand
       * @return {Command} `this` command for chaining
       */
      copyInheritedSettings(sourceCommand) {
        this._outputConfiguration = sourceCommand._outputConfiguration;
        this._helpOption = sourceCommand._helpOption;
        this._helpCommand = sourceCommand._helpCommand;
        this._helpConfiguration = sourceCommand._helpConfiguration;
        this._exitCallback = sourceCommand._exitCallback;
        this._storeOptionsAsProperties = sourceCommand._storeOptionsAsProperties;
        this._combineFlagAndOptionalValue = sourceCommand._combineFlagAndOptionalValue;
        this._allowExcessArguments = sourceCommand._allowExcessArguments;
        this._enablePositionalOptions = sourceCommand._enablePositionalOptions;
        this._showHelpAfterError = sourceCommand._showHelpAfterError;
        this._showSuggestionAfterError = sourceCommand._showSuggestionAfterError;
        return this;
      }
      /**
       * @returns {Command[]}
       * @private
       */
      _getCommandAndAncestors() {
        const result = [];
        for (let command = this; command; command = command.parent) {
          result.push(command);
        }
        return result;
      }
      /**
       * Define a command.
       *
       * There are two styles of command: pay attention to where to put the description.
       *
       * @example
       * // Command implemented using action handler (description is supplied separately to `.command`)
       * program
       *   .command('clone <source> [destination]')
       *   .description('clone a repository into a newly created directory')
       *   .action((source, destination) => {
       *     console.log('clone command called');
       *   });
       *
       * // Command implemented using separate executable file (description is second parameter to `.command`)
       * program
       *   .command('start <service>', 'start named service')
       *   .command('stop [service]', 'stop named service, or all if no name supplied');
       *
       * @param {string} nameAndArgs - command name and arguments, args are `<required>` or `[optional]` and last may also be `variadic...`
       * @param {(object | string)} [actionOptsOrExecDesc] - configuration options (for action), or description (for executable)
       * @param {object} [execOpts] - configuration options (for executable)
       * @return {Command} returns new command for action handler, or `this` for executable command
       */
      command(nameAndArgs, actionOptsOrExecDesc, execOpts) {
        let desc = actionOptsOrExecDesc;
        let opts = execOpts;
        if (typeof desc === "object" && desc !== null) {
          opts = desc;
          desc = null;
        }
        opts = opts || {};
        const [, name, args] = nameAndArgs.match(/([^ ]+) *(.*)/);
        const cmd = this.createCommand(name);
        if (desc) {
          cmd.description(desc);
          cmd._executableHandler = true;
        }
        if (opts.isDefault) this._defaultCommandName = cmd._name;
        cmd._hidden = !!(opts.noHelp || opts.hidden);
        cmd._executableFile = opts.executableFile || null;
        if (args) cmd.arguments(args);
        this._registerCommand(cmd);
        cmd.parent = this;
        cmd.copyInheritedSettings(this);
        if (desc) return this;
        return cmd;
      }
      /**
       * Factory routine to create a new unattached command.
       *
       * See .command() for creating an attached subcommand, which uses this routine to
       * create the command. You can override createCommand to customise subcommands.
       *
       * @param {string} [name]
       * @return {Command} new command
       */
      createCommand(name) {
        return new _Command(name);
      }
      /**
       * You can customise the help with a subclass of Help by overriding createHelp,
       * or by overriding Help properties using configureHelp().
       *
       * @return {Help}
       */
      createHelp() {
        return Object.assign(new Help2(), this.configureHelp());
      }
      /**
       * You can customise the help by overriding Help properties using configureHelp(),
       * or with a subclass of Help by overriding createHelp().
       *
       * @param {object} [configuration] - configuration options
       * @return {(Command | object)} `this` command for chaining, or stored configuration
       */
      configureHelp(configuration) {
        if (configuration === void 0) return this._helpConfiguration;
        this._helpConfiguration = configuration;
        return this;
      }
      /**
       * The default output goes to stdout and stderr. You can customise this for special
       * applications. You can also customise the display of errors by overriding outputError.
       *
       * The configuration properties are all functions:
       *
       *     // functions to change where being written, stdout and stderr
       *     writeOut(str)
       *     writeErr(str)
       *     // matching functions to specify width for wrapping help
       *     getOutHelpWidth()
       *     getErrHelpWidth()
       *     // functions based on what is being written out
       *     outputError(str, write) // used for displaying errors, and not used for displaying help
       *
       * @param {object} [configuration] - configuration options
       * @return {(Command | object)} `this` command for chaining, or stored configuration
       */
      configureOutput(configuration) {
        if (configuration === void 0) return this._outputConfiguration;
        Object.assign(this._outputConfiguration, configuration);
        return this;
      }
      /**
       * Display the help or a custom message after an error occurs.
       *
       * @param {(boolean|string)} [displayHelp]
       * @return {Command} `this` command for chaining
       */
      showHelpAfterError(displayHelp = true) {
        if (typeof displayHelp !== "string") displayHelp = !!displayHelp;
        this._showHelpAfterError = displayHelp;
        return this;
      }
      /**
       * Display suggestion of similar commands for unknown commands, or options for unknown options.
       *
       * @param {boolean} [displaySuggestion]
       * @return {Command} `this` command for chaining
       */
      showSuggestionAfterError(displaySuggestion = true) {
        this._showSuggestionAfterError = !!displaySuggestion;
        return this;
      }
      /**
       * Add a prepared subcommand.
       *
       * See .command() for creating an attached subcommand which inherits settings from its parent.
       *
       * @param {Command} cmd - new subcommand
       * @param {object} [opts] - configuration options
       * @return {Command} `this` command for chaining
       */
      addCommand(cmd, opts) {
        if (!cmd._name) {
          throw new Error(`Command passed to .addCommand() must have a name
- specify the name in Command constructor or using .name()`);
        }
        opts = opts || {};
        if (opts.isDefault) this._defaultCommandName = cmd._name;
        if (opts.noHelp || opts.hidden) cmd._hidden = true;
        this._registerCommand(cmd);
        cmd.parent = this;
        cmd._checkForBrokenPassThrough();
        return this;
      }
      /**
       * Factory routine to create a new unattached argument.
       *
       * See .argument() for creating an attached argument, which uses this routine to
       * create the argument. You can override createArgument to return a custom argument.
       *
       * @param {string} name
       * @param {string} [description]
       * @return {Argument} new argument
       */
      createArgument(name, description) {
        return new Argument2(name, description);
      }
      /**
       * Define argument syntax for command.
       *
       * The default is that the argument is required, and you can explicitly
       * indicate this with <> around the name. Put [] around the name for an optional argument.
       *
       * @example
       * program.argument('<input-file>');
       * program.argument('[output-file]');
       *
       * @param {string} name
       * @param {string} [description]
       * @param {(Function|*)} [fn] - custom argument processing function
       * @param {*} [defaultValue]
       * @return {Command} `this` command for chaining
       */
      argument(name, description, fn, defaultValue) {
        const argument = this.createArgument(name, description);
        if (typeof fn === "function") {
          argument.default(defaultValue).argParser(fn);
        } else {
          argument.default(fn);
        }
        this.addArgument(argument);
        return this;
      }
      /**
       * Define argument syntax for command, adding multiple at once (without descriptions).
       *
       * See also .argument().
       *
       * @example
       * program.arguments('<cmd> [env]');
       *
       * @param {string} names
       * @return {Command} `this` command for chaining
       */
      arguments(names) {
        names.trim().split(/ +/).forEach((detail) => {
          this.argument(detail);
        });
        return this;
      }
      /**
       * Define argument syntax for command, adding a prepared argument.
       *
       * @param {Argument} argument
       * @return {Command} `this` command for chaining
       */
      addArgument(argument) {
        const previousArgument = this.registeredArguments.slice(-1)[0];
        if (previousArgument && previousArgument.variadic) {
          throw new Error(
            `only the last argument can be variadic '${previousArgument.name()}'`
          );
        }
        if (argument.required && argument.defaultValue !== void 0 && argument.parseArg === void 0) {
          throw new Error(
            `a default value for a required argument is never used: '${argument.name()}'`
          );
        }
        this.registeredArguments.push(argument);
        return this;
      }
      /**
       * Customise or override default help command. By default a help command is automatically added if your command has subcommands.
       *
       * @example
       *    program.helpCommand('help [cmd]');
       *    program.helpCommand('help [cmd]', 'show help');
       *    program.helpCommand(false); // suppress default help command
       *    program.helpCommand(true); // add help command even if no subcommands
       *
       * @param {string|boolean} enableOrNameAndArgs - enable with custom name and/or arguments, or boolean to override whether added
       * @param {string} [description] - custom description
       * @return {Command} `this` command for chaining
       */
      helpCommand(enableOrNameAndArgs, description) {
        if (typeof enableOrNameAndArgs === "boolean") {
          this._addImplicitHelpCommand = enableOrNameAndArgs;
          return this;
        }
        enableOrNameAndArgs = enableOrNameAndArgs ?? "help [command]";
        const [, helpName, helpArgs] = enableOrNameAndArgs.match(/([^ ]+) *(.*)/);
        const helpDescription = description ?? "display help for command";
        const helpCommand = this.createCommand(helpName);
        helpCommand.helpOption(false);
        if (helpArgs) helpCommand.arguments(helpArgs);
        if (helpDescription) helpCommand.description(helpDescription);
        this._addImplicitHelpCommand = true;
        this._helpCommand = helpCommand;
        return this;
      }
      /**
       * Add prepared custom help command.
       *
       * @param {(Command|string|boolean)} helpCommand - custom help command, or deprecated enableOrNameAndArgs as for `.helpCommand()`
       * @param {string} [deprecatedDescription] - deprecated custom description used with custom name only
       * @return {Command} `this` command for chaining
       */
      addHelpCommand(helpCommand, deprecatedDescription) {
        if (typeof helpCommand !== "object") {
          this.helpCommand(helpCommand, deprecatedDescription);
          return this;
        }
        this._addImplicitHelpCommand = true;
        this._helpCommand = helpCommand;
        return this;
      }
      /**
       * Lazy create help command.
       *
       * @return {(Command|null)}
       * @package
       */
      _getHelpCommand() {
        const hasImplicitHelpCommand = this._addImplicitHelpCommand ?? (this.commands.length && !this._actionHandler && !this._findCommand("help"));
        if (hasImplicitHelpCommand) {
          if (this._helpCommand === void 0) {
            this.helpCommand(void 0, void 0);
          }
          return this._helpCommand;
        }
        return null;
      }
      /**
       * Add hook for life cycle event.
       *
       * @param {string} event
       * @param {Function} listener
       * @return {Command} `this` command for chaining
       */
      hook(event, listener) {
        const allowedValues = ["preSubcommand", "preAction", "postAction"];
        if (!allowedValues.includes(event)) {
          throw new Error(`Unexpected value for event passed to hook : '${event}'.
Expecting one of '${allowedValues.join("', '")}'`);
        }
        if (this._lifeCycleHooks[event]) {
          this._lifeCycleHooks[event].push(listener);
        } else {
          this._lifeCycleHooks[event] = [listener];
        }
        return this;
      }
      /**
       * Register callback to use as replacement for calling process.exit.
       *
       * @param {Function} [fn] optional callback which will be passed a CommanderError, defaults to throwing
       * @return {Command} `this` command for chaining
       */
      exitOverride(fn) {
        if (fn) {
          this._exitCallback = fn;
        } else {
          this._exitCallback = (err2) => {
            if (err2.code !== "commander.executeSubCommandAsync") {
              throw err2;
            } else {
            }
          };
        }
        return this;
      }
      /**
       * Call process.exit, and _exitCallback if defined.
       *
       * @param {number} exitCode exit code for using with process.exit
       * @param {string} code an id string representing the error
       * @param {string} message human-readable description of the error
       * @return never
       * @private
       */
      _exit(exitCode, code, message) {
        if (this._exitCallback) {
          this._exitCallback(new CommanderError2(exitCode, code, message));
        }
        process8.exit(exitCode);
      }
      /**
       * Register callback `fn` for the command.
       *
       * @example
       * program
       *   .command('serve')
       *   .description('start service')
       *   .action(function() {
       *      // do work here
       *   });
       *
       * @param {Function} fn
       * @return {Command} `this` command for chaining
       */
      action(fn) {
        const listener = (args) => {
          const expectedArgsCount = this.registeredArguments.length;
          const actionArgs = args.slice(0, expectedArgsCount);
          if (this._storeOptionsAsProperties) {
            actionArgs[expectedArgsCount] = this;
          } else {
            actionArgs[expectedArgsCount] = this.opts();
          }
          actionArgs.push(this);
          return fn.apply(this, actionArgs);
        };
        this._actionHandler = listener;
        return this;
      }
      /**
       * Factory routine to create a new unattached option.
       *
       * See .option() for creating an attached option, which uses this routine to
       * create the option. You can override createOption to return a custom option.
       *
       * @param {string} flags
       * @param {string} [description]
       * @return {Option} new option
       */
      createOption(flags, description) {
        return new Option2(flags, description);
      }
      /**
       * Wrap parseArgs to catch 'commander.invalidArgument'.
       *
       * @param {(Option | Argument)} target
       * @param {string} value
       * @param {*} previous
       * @param {string} invalidArgumentMessage
       * @private
       */
      _callParseArg(target, value, previous, invalidArgumentMessage) {
        try {
          return target.parseArg(value, previous);
        } catch (err2) {
          if (err2.code === "commander.invalidArgument") {
            const message = `${invalidArgumentMessage} ${err2.message}`;
            this.error(message, { exitCode: err2.exitCode, code: err2.code });
          }
          throw err2;
        }
      }
      /**
       * Check for option flag conflicts.
       * Register option if no conflicts found, or throw on conflict.
       *
       * @param {Option} option
       * @private
       */
      _registerOption(option) {
        const matchingOption = option.short && this._findOption(option.short) || option.long && this._findOption(option.long);
        if (matchingOption) {
          const matchingFlag = option.long && this._findOption(option.long) ? option.long : option.short;
          throw new Error(`Cannot add option '${option.flags}'${this._name && ` to command '${this._name}'`} due to conflicting flag '${matchingFlag}'
-  already used by option '${matchingOption.flags}'`);
        }
        this.options.push(option);
      }
      /**
       * Check for command name and alias conflicts with existing commands.
       * Register command if no conflicts found, or throw on conflict.
       *
       * @param {Command} command
       * @private
       */
      _registerCommand(command) {
        const knownBy = (cmd) => {
          return [cmd.name()].concat(cmd.aliases());
        };
        const alreadyUsed = knownBy(command).find(
          (name) => this._findCommand(name)
        );
        if (alreadyUsed) {
          const existingCmd = knownBy(this._findCommand(alreadyUsed)).join("|");
          const newCmd = knownBy(command).join("|");
          throw new Error(
            `cannot add command '${newCmd}' as already have command '${existingCmd}'`
          );
        }
        this.commands.push(command);
      }
      /**
       * Add an option.
       *
       * @param {Option} option
       * @return {Command} `this` command for chaining
       */
      addOption(option) {
        this._registerOption(option);
        const oname = option.name();
        const name = option.attributeName();
        if (option.negate) {
          const positiveLongFlag = option.long.replace(/^--no-/, "--");
          if (!this._findOption(positiveLongFlag)) {
            this.setOptionValueWithSource(
              name,
              option.defaultValue === void 0 ? true : option.defaultValue,
              "default"
            );
          }
        } else if (option.defaultValue !== void 0) {
          this.setOptionValueWithSource(name, option.defaultValue, "default");
        }
        const handleOptionValue = (val, invalidValueMessage, valueSource) => {
          if (val == null && option.presetArg !== void 0) {
            val = option.presetArg;
          }
          const oldValue = this.getOptionValue(name);
          if (val !== null && option.parseArg) {
            val = this._callParseArg(option, val, oldValue, invalidValueMessage);
          } else if (val !== null && option.variadic) {
            val = option._concatValue(val, oldValue);
          }
          if (val == null) {
            if (option.negate) {
              val = false;
            } else if (option.isBoolean() || option.optional) {
              val = true;
            } else {
              val = "";
            }
          }
          this.setOptionValueWithSource(name, val, valueSource);
        };
        this.on("option:" + oname, (val) => {
          const invalidValueMessage = `error: option '${option.flags}' argument '${val}' is invalid.`;
          handleOptionValue(val, invalidValueMessage, "cli");
        });
        if (option.envVar) {
          this.on("optionEnv:" + oname, (val) => {
            const invalidValueMessage = `error: option '${option.flags}' value '${val}' from env '${option.envVar}' is invalid.`;
            handleOptionValue(val, invalidValueMessage, "env");
          });
        }
        return this;
      }
      /**
       * Internal implementation shared by .option() and .requiredOption()
       *
       * @return {Command} `this` command for chaining
       * @private
       */
      _optionEx(config, flags, description, fn, defaultValue) {
        if (typeof flags === "object" && flags instanceof Option2) {
          throw new Error(
            "To add an Option object use addOption() instead of option() or requiredOption()"
          );
        }
        const option = this.createOption(flags, description);
        option.makeOptionMandatory(!!config.mandatory);
        if (typeof fn === "function") {
          option.default(defaultValue).argParser(fn);
        } else if (fn instanceof RegExp) {
          const regex = fn;
          fn = (val, def) => {
            const m = regex.exec(val);
            return m ? m[0] : def;
          };
          option.default(defaultValue).argParser(fn);
        } else {
          option.default(fn);
        }
        return this.addOption(option);
      }
      /**
       * Define option with `flags`, `description`, and optional argument parsing function or `defaultValue` or both.
       *
       * The `flags` string contains the short and/or long flags, separated by comma, a pipe or space. A required
       * option-argument is indicated by `<>` and an optional option-argument by `[]`.
       *
       * See the README for more details, and see also addOption() and requiredOption().
       *
       * @example
       * program
       *     .option('-p, --pepper', 'add pepper')
       *     .option('-p, --pizza-type <TYPE>', 'type of pizza') // required option-argument
       *     .option('-c, --cheese [CHEESE]', 'add extra cheese', 'mozzarella') // optional option-argument with default
       *     .option('-t, --tip <VALUE>', 'add tip to purchase cost', parseFloat) // custom parse function
       *
       * @param {string} flags
       * @param {string} [description]
       * @param {(Function|*)} [parseArg] - custom option processing function or default value
       * @param {*} [defaultValue]
       * @return {Command} `this` command for chaining
       */
      option(flags, description, parseArg, defaultValue) {
        return this._optionEx({}, flags, description, parseArg, defaultValue);
      }
      /**
       * Add a required option which must have a value after parsing. This usually means
       * the option must be specified on the command line. (Otherwise the same as .option().)
       *
       * The `flags` string contains the short and/or long flags, separated by comma, a pipe or space.
       *
       * @param {string} flags
       * @param {string} [description]
       * @param {(Function|*)} [parseArg] - custom option processing function or default value
       * @param {*} [defaultValue]
       * @return {Command} `this` command for chaining
       */
      requiredOption(flags, description, parseArg, defaultValue) {
        return this._optionEx(
          { mandatory: true },
          flags,
          description,
          parseArg,
          defaultValue
        );
      }
      /**
       * Alter parsing of short flags with optional values.
       *
       * @example
       * // for `.option('-f,--flag [value]'):
       * program.combineFlagAndOptionalValue(true);  // `-f80` is treated like `--flag=80`, this is the default behaviour
       * program.combineFlagAndOptionalValue(false) // `-fb` is treated like `-f -b`
       *
       * @param {boolean} [combine] - if `true` or omitted, an optional value can be specified directly after the flag.
       * @return {Command} `this` command for chaining
       */
      combineFlagAndOptionalValue(combine = true) {
        this._combineFlagAndOptionalValue = !!combine;
        return this;
      }
      /**
       * Allow unknown options on the command line.
       *
       * @param {boolean} [allowUnknown] - if `true` or omitted, no error will be thrown for unknown options.
       * @return {Command} `this` command for chaining
       */
      allowUnknownOption(allowUnknown = true) {
        this._allowUnknownOption = !!allowUnknown;
        return this;
      }
      /**
       * Allow excess command-arguments on the command line. Pass false to make excess arguments an error.
       *
       * @param {boolean} [allowExcess] - if `true` or omitted, no error will be thrown for excess arguments.
       * @return {Command} `this` command for chaining
       */
      allowExcessArguments(allowExcess = true) {
        this._allowExcessArguments = !!allowExcess;
        return this;
      }
      /**
       * Enable positional options. Positional means global options are specified before subcommands which lets
       * subcommands reuse the same option names, and also enables subcommands to turn on passThroughOptions.
       * The default behaviour is non-positional and global options may appear anywhere on the command line.
       *
       * @param {boolean} [positional]
       * @return {Command} `this` command for chaining
       */
      enablePositionalOptions(positional = true) {
        this._enablePositionalOptions = !!positional;
        return this;
      }
      /**
       * Pass through options that come after command-arguments rather than treat them as command-options,
       * so actual command-options come before command-arguments. Turning this on for a subcommand requires
       * positional options to have been enabled on the program (parent commands).
       * The default behaviour is non-positional and options may appear before or after command-arguments.
       *
       * @param {boolean} [passThrough] for unknown options.
       * @return {Command} `this` command for chaining
       */
      passThroughOptions(passThrough = true) {
        this._passThroughOptions = !!passThrough;
        this._checkForBrokenPassThrough();
        return this;
      }
      /**
       * @private
       */
      _checkForBrokenPassThrough() {
        if (this.parent && this._passThroughOptions && !this.parent._enablePositionalOptions) {
          throw new Error(
            `passThroughOptions cannot be used for '${this._name}' without turning on enablePositionalOptions for parent command(s)`
          );
        }
      }
      /**
       * Whether to store option values as properties on command object,
       * or store separately (specify false). In both cases the option values can be accessed using .opts().
       *
       * @param {boolean} [storeAsProperties=true]
       * @return {Command} `this` command for chaining
       */
      storeOptionsAsProperties(storeAsProperties = true) {
        if (this.options.length) {
          throw new Error("call .storeOptionsAsProperties() before adding options");
        }
        if (Object.keys(this._optionValues).length) {
          throw new Error(
            "call .storeOptionsAsProperties() before setting option values"
          );
        }
        this._storeOptionsAsProperties = !!storeAsProperties;
        return this;
      }
      /**
       * Retrieve option value.
       *
       * @param {string} key
       * @return {object} value
       */
      getOptionValue(key) {
        if (this._storeOptionsAsProperties) {
          return this[key];
        }
        return this._optionValues[key];
      }
      /**
       * Store option value.
       *
       * @param {string} key
       * @param {object} value
       * @return {Command} `this` command for chaining
       */
      setOptionValue(key, value) {
        return this.setOptionValueWithSource(key, value, void 0);
      }
      /**
       * Store option value and where the value came from.
       *
       * @param {string} key
       * @param {object} value
       * @param {string} source - expected values are default/config/env/cli/implied
       * @return {Command} `this` command for chaining
       */
      setOptionValueWithSource(key, value, source) {
        if (this._storeOptionsAsProperties) {
          this[key] = value;
        } else {
          this._optionValues[key] = value;
        }
        this._optionValueSources[key] = source;
        return this;
      }
      /**
       * Get source of option value.
       * Expected values are default | config | env | cli | implied
       *
       * @param {string} key
       * @return {string}
       */
      getOptionValueSource(key) {
        return this._optionValueSources[key];
      }
      /**
       * Get source of option value. See also .optsWithGlobals().
       * Expected values are default | config | env | cli | implied
       *
       * @param {string} key
       * @return {string}
       */
      getOptionValueSourceWithGlobals(key) {
        let source;
        this._getCommandAndAncestors().forEach((cmd) => {
          if (cmd.getOptionValueSource(key) !== void 0) {
            source = cmd.getOptionValueSource(key);
          }
        });
        return source;
      }
      /**
       * Get user arguments from implied or explicit arguments.
       * Side-effects: set _scriptPath if args included script. Used for default program name, and subcommand searches.
       *
       * @private
       */
      _prepareUserArgs(argv, parseOptions) {
        if (argv !== void 0 && !Array.isArray(argv)) {
          throw new Error("first parameter to parse must be array or undefined");
        }
        parseOptions = parseOptions || {};
        if (argv === void 0 && parseOptions.from === void 0) {
          if (process8.versions?.electron) {
            parseOptions.from = "electron";
          }
          const execArgv = process8.execArgv ?? [];
          if (execArgv.includes("-e") || execArgv.includes("--eval") || execArgv.includes("-p") || execArgv.includes("--print")) {
            parseOptions.from = "eval";
          }
        }
        if (argv === void 0) {
          argv = process8.argv;
        }
        this.rawArgs = argv.slice();
        let userArgs;
        switch (parseOptions.from) {
          case void 0:
          case "node":
            this._scriptPath = argv[1];
            userArgs = argv.slice(2);
            break;
          case "electron":
            if (process8.defaultApp) {
              this._scriptPath = argv[1];
              userArgs = argv.slice(2);
            } else {
              userArgs = argv.slice(1);
            }
            break;
          case "user":
            userArgs = argv.slice(0);
            break;
          case "eval":
            userArgs = argv.slice(1);
            break;
          default:
            throw new Error(
              `unexpected parse option { from: '${parseOptions.from}' }`
            );
        }
        if (!this._name && this._scriptPath)
          this.nameFromFilename(this._scriptPath);
        this._name = this._name || "program";
        return userArgs;
      }
      /**
       * Parse `argv`, setting options and invoking commands when defined.
       *
       * Use parseAsync instead of parse if any of your action handlers are async.
       *
       * Call with no parameters to parse `process.argv`. Detects Electron and special node options like `node --eval`. Easy mode!
       *
       * Or call with an array of strings to parse, and optionally where the user arguments start by specifying where the arguments are `from`:
       * - `'node'`: default, `argv[0]` is the application and `argv[1]` is the script being run, with user arguments after that
       * - `'electron'`: `argv[0]` is the application and `argv[1]` varies depending on whether the electron application is packaged
       * - `'user'`: just user arguments
       *
       * @example
       * program.parse(); // parse process.argv and auto-detect electron and special node flags
       * program.parse(process.argv); // assume argv[0] is app and argv[1] is script
       * program.parse(my-args, { from: 'user' }); // just user supplied arguments, nothing special about argv[0]
       *
       * @param {string[]} [argv] - optional, defaults to process.argv
       * @param {object} [parseOptions] - optionally specify style of options with from: node/user/electron
       * @param {string} [parseOptions.from] - where the args are from: 'node', 'user', 'electron'
       * @return {Command} `this` command for chaining
       */
      parse(argv, parseOptions) {
        const userArgs = this._prepareUserArgs(argv, parseOptions);
        this._parseCommand([], userArgs);
        return this;
      }
      /**
       * Parse `argv`, setting options and invoking commands when defined.
       *
       * Call with no parameters to parse `process.argv`. Detects Electron and special node options like `node --eval`. Easy mode!
       *
       * Or call with an array of strings to parse, and optionally where the user arguments start by specifying where the arguments are `from`:
       * - `'node'`: default, `argv[0]` is the application and `argv[1]` is the script being run, with user arguments after that
       * - `'electron'`: `argv[0]` is the application and `argv[1]` varies depending on whether the electron application is packaged
       * - `'user'`: just user arguments
       *
       * @example
       * await program.parseAsync(); // parse process.argv and auto-detect electron and special node flags
       * await program.parseAsync(process.argv); // assume argv[0] is app and argv[1] is script
       * await program.parseAsync(my-args, { from: 'user' }); // just user supplied arguments, nothing special about argv[0]
       *
       * @param {string[]} [argv]
       * @param {object} [parseOptions]
       * @param {string} parseOptions.from - where the args are from: 'node', 'user', 'electron'
       * @return {Promise}
       */
      async parseAsync(argv, parseOptions) {
        const userArgs = this._prepareUserArgs(argv, parseOptions);
        await this._parseCommand([], userArgs);
        return this;
      }
      /**
       * Execute a sub-command executable.
       *
       * @private
       */
      _executeSubCommand(subcommand, args) {
        args = args.slice();
        let launchWithNode = false;
        const sourceExt = [".js", ".ts", ".tsx", ".mjs", ".cjs"];
        function findFile(baseDir, baseName) {
          const localBin = path13.resolve(baseDir, baseName);
          if (fs16.existsSync(localBin)) return localBin;
          if (sourceExt.includes(path13.extname(baseName))) return void 0;
          const foundExt = sourceExt.find(
            (ext) => fs16.existsSync(`${localBin}${ext}`)
          );
          if (foundExt) return `${localBin}${foundExt}`;
          return void 0;
        }
        this._checkForMissingMandatoryOptions();
        this._checkForConflictingOptions();
        let executableFile = subcommand._executableFile || `${this._name}-${subcommand._name}`;
        let executableDir = this._executableDir || "";
        if (this._scriptPath) {
          let resolvedScriptPath;
          try {
            resolvedScriptPath = fs16.realpathSync(this._scriptPath);
          } catch (err2) {
            resolvedScriptPath = this._scriptPath;
          }
          executableDir = path13.resolve(
            path13.dirname(resolvedScriptPath),
            executableDir
          );
        }
        if (executableDir) {
          let localFile = findFile(executableDir, executableFile);
          if (!localFile && !subcommand._executableFile && this._scriptPath) {
            const legacyName = path13.basename(
              this._scriptPath,
              path13.extname(this._scriptPath)
            );
            if (legacyName !== this._name) {
              localFile = findFile(
                executableDir,
                `${legacyName}-${subcommand._name}`
              );
            }
          }
          executableFile = localFile || executableFile;
        }
        launchWithNode = sourceExt.includes(path13.extname(executableFile));
        let proc;
        if (process8.platform !== "win32") {
          if (launchWithNode) {
            args.unshift(executableFile);
            args = incrementNodeInspectorPort(process8.execArgv).concat(args);
            proc = childProcess2.spawn(process8.argv[0], args, { stdio: "inherit" });
          } else {
            proc = childProcess2.spawn(executableFile, args, { stdio: "inherit" });
          }
        } else {
          args.unshift(executableFile);
          args = incrementNodeInspectorPort(process8.execArgv).concat(args);
          proc = childProcess2.spawn(process8.execPath, args, { stdio: "inherit" });
        }
        if (!proc.killed) {
          const signals = ["SIGUSR1", "SIGUSR2", "SIGTERM", "SIGINT", "SIGHUP"];
          signals.forEach((signal) => {
            process8.on(signal, () => {
              if (proc.killed === false && proc.exitCode === null) {
                proc.kill(signal);
              }
            });
          });
        }
        const exitCallback = this._exitCallback;
        proc.on("close", (code) => {
          code = code ?? 1;
          if (!exitCallback) {
            process8.exit(code);
          } else {
            exitCallback(
              new CommanderError2(
                code,
                "commander.executeSubCommandAsync",
                "(close)"
              )
            );
          }
        });
        proc.on("error", (err2) => {
          if (err2.code === "ENOENT") {
            const executableDirMessage = executableDir ? `searched for local subcommand relative to directory '${executableDir}'` : "no directory for search for local subcommand, use .executableDir() to supply a custom directory";
            const executableMissing = `'${executableFile}' does not exist
 - if '${subcommand._name}' is not meant to be an executable command, remove description parameter from '.command()' and use '.description()' instead
 - if the default executable name is not suitable, use the executableFile option to supply a custom name or path
 - ${executableDirMessage}`;
            throw new Error(executableMissing);
          } else if (err2.code === "EACCES") {
            throw new Error(`'${executableFile}' not executable`);
          }
          if (!exitCallback) {
            process8.exit(1);
          } else {
            const wrappedError = new CommanderError2(
              1,
              "commander.executeSubCommandAsync",
              "(error)"
            );
            wrappedError.nestedError = err2;
            exitCallback(wrappedError);
          }
        });
        this.runningCommand = proc;
      }
      /**
       * @private
       */
      _dispatchSubcommand(commandName, operands, unknown) {
        const subCommand = this._findCommand(commandName);
        if (!subCommand) this.help({ error: true });
        let promiseChain;
        promiseChain = this._chainOrCallSubCommandHook(
          promiseChain,
          subCommand,
          "preSubcommand"
        );
        promiseChain = this._chainOrCall(promiseChain, () => {
          if (subCommand._executableHandler) {
            this._executeSubCommand(subCommand, operands.concat(unknown));
          } else {
            return subCommand._parseCommand(operands, unknown);
          }
        });
        return promiseChain;
      }
      /**
       * Invoke help directly if possible, or dispatch if necessary.
       * e.g. help foo
       *
       * @private
       */
      _dispatchHelpCommand(subcommandName) {
        if (!subcommandName) {
          this.help();
        }
        const subCommand = this._findCommand(subcommandName);
        if (subCommand && !subCommand._executableHandler) {
          subCommand.help();
        }
        return this._dispatchSubcommand(
          subcommandName,
          [],
          [this._getHelpOption()?.long ?? this._getHelpOption()?.short ?? "--help"]
        );
      }
      /**
       * Check this.args against expected this.registeredArguments.
       *
       * @private
       */
      _checkNumberOfArguments() {
        this.registeredArguments.forEach((arg, i) => {
          if (arg.required && this.args[i] == null) {
            this.missingArgument(arg.name());
          }
        });
        if (this.registeredArguments.length > 0 && this.registeredArguments[this.registeredArguments.length - 1].variadic) {
          return;
        }
        if (this.args.length > this.registeredArguments.length) {
          this._excessArguments(this.args);
        }
      }
      /**
       * Process this.args using this.registeredArguments and save as this.processedArgs!
       *
       * @private
       */
      _processArguments() {
        const myParseArg = (argument, value, previous) => {
          let parsedValue = value;
          if (value !== null && argument.parseArg) {
            const invalidValueMessage = `error: command-argument value '${value}' is invalid for argument '${argument.name()}'.`;
            parsedValue = this._callParseArg(
              argument,
              value,
              previous,
              invalidValueMessage
            );
          }
          return parsedValue;
        };
        this._checkNumberOfArguments();
        const processedArgs = [];
        this.registeredArguments.forEach((declaredArg, index) => {
          let value = declaredArg.defaultValue;
          if (declaredArg.variadic) {
            if (index < this.args.length) {
              value = this.args.slice(index);
              if (declaredArg.parseArg) {
                value = value.reduce((processed, v) => {
                  return myParseArg(declaredArg, v, processed);
                }, declaredArg.defaultValue);
              }
            } else if (value === void 0) {
              value = [];
            }
          } else if (index < this.args.length) {
            value = this.args[index];
            if (declaredArg.parseArg) {
              value = myParseArg(declaredArg, value, declaredArg.defaultValue);
            }
          }
          processedArgs[index] = value;
        });
        this.processedArgs = processedArgs;
      }
      /**
       * Once we have a promise we chain, but call synchronously until then.
       *
       * @param {(Promise|undefined)} promise
       * @param {Function} fn
       * @return {(Promise|undefined)}
       * @private
       */
      _chainOrCall(promise, fn) {
        if (promise && promise.then && typeof promise.then === "function") {
          return promise.then(() => fn());
        }
        return fn();
      }
      /**
       *
       * @param {(Promise|undefined)} promise
       * @param {string} event
       * @return {(Promise|undefined)}
       * @private
       */
      _chainOrCallHooks(promise, event) {
        let result = promise;
        const hooks = [];
        this._getCommandAndAncestors().reverse().filter((cmd) => cmd._lifeCycleHooks[event] !== void 0).forEach((hookedCommand) => {
          hookedCommand._lifeCycleHooks[event].forEach((callback) => {
            hooks.push({ hookedCommand, callback });
          });
        });
        if (event === "postAction") {
          hooks.reverse();
        }
        hooks.forEach((hookDetail) => {
          result = this._chainOrCall(result, () => {
            return hookDetail.callback(hookDetail.hookedCommand, this);
          });
        });
        return result;
      }
      /**
       *
       * @param {(Promise|undefined)} promise
       * @param {Command} subCommand
       * @param {string} event
       * @return {(Promise|undefined)}
       * @private
       */
      _chainOrCallSubCommandHook(promise, subCommand, event) {
        let result = promise;
        if (this._lifeCycleHooks[event] !== void 0) {
          this._lifeCycleHooks[event].forEach((hook) => {
            result = this._chainOrCall(result, () => {
              return hook(this, subCommand);
            });
          });
        }
        return result;
      }
      /**
       * Process arguments in context of this command.
       * Returns action result, in case it is a promise.
       *
       * @private
       */
      _parseCommand(operands, unknown) {
        const parsed = this.parseOptions(unknown);
        this._parseOptionsEnv();
        this._parseOptionsImplied();
        operands = operands.concat(parsed.operands);
        unknown = parsed.unknown;
        this.args = operands.concat(unknown);
        if (operands && this._findCommand(operands[0])) {
          return this._dispatchSubcommand(operands[0], operands.slice(1), unknown);
        }
        if (this._getHelpCommand() && operands[0] === this._getHelpCommand().name()) {
          return this._dispatchHelpCommand(operands[1]);
        }
        if (this._defaultCommandName) {
          this._outputHelpIfRequested(unknown);
          return this._dispatchSubcommand(
            this._defaultCommandName,
            operands,
            unknown
          );
        }
        if (this.commands.length && this.args.length === 0 && !this._actionHandler && !this._defaultCommandName) {
          this.help({ error: true });
        }
        this._outputHelpIfRequested(parsed.unknown);
        this._checkForMissingMandatoryOptions();
        this._checkForConflictingOptions();
        const checkForUnknownOptions = () => {
          if (parsed.unknown.length > 0) {
            this.unknownOption(parsed.unknown[0]);
          }
        };
        const commandEvent = `command:${this.name()}`;
        if (this._actionHandler) {
          checkForUnknownOptions();
          this._processArguments();
          let promiseChain;
          promiseChain = this._chainOrCallHooks(promiseChain, "preAction");
          promiseChain = this._chainOrCall(
            promiseChain,
            () => this._actionHandler(this.processedArgs)
          );
          if (this.parent) {
            promiseChain = this._chainOrCall(promiseChain, () => {
              this.parent.emit(commandEvent, operands, unknown);
            });
          }
          promiseChain = this._chainOrCallHooks(promiseChain, "postAction");
          return promiseChain;
        }
        if (this.parent && this.parent.listenerCount(commandEvent)) {
          checkForUnknownOptions();
          this._processArguments();
          this.parent.emit(commandEvent, operands, unknown);
        } else if (operands.length) {
          if (this._findCommand("*")) {
            return this._dispatchSubcommand("*", operands, unknown);
          }
          if (this.listenerCount("command:*")) {
            this.emit("command:*", operands, unknown);
          } else if (this.commands.length) {
            this.unknownCommand();
          } else {
            checkForUnknownOptions();
            this._processArguments();
          }
        } else if (this.commands.length) {
          checkForUnknownOptions();
          this.help({ error: true });
        } else {
          checkForUnknownOptions();
          this._processArguments();
        }
      }
      /**
       * Find matching command.
       *
       * @private
       * @return {Command | undefined}
       */
      _findCommand(name) {
        if (!name) return void 0;
        return this.commands.find(
          (cmd) => cmd._name === name || cmd._aliases.includes(name)
        );
      }
      /**
       * Return an option matching `arg` if any.
       *
       * @param {string} arg
       * @return {Option}
       * @package
       */
      _findOption(arg) {
        return this.options.find((option) => option.is(arg));
      }
      /**
       * Display an error message if a mandatory option does not have a value.
       * Called after checking for help flags in leaf subcommand.
       *
       * @private
       */
      _checkForMissingMandatoryOptions() {
        this._getCommandAndAncestors().forEach((cmd) => {
          cmd.options.forEach((anOption) => {
            if (anOption.mandatory && cmd.getOptionValue(anOption.attributeName()) === void 0) {
              cmd.missingMandatoryOptionValue(anOption);
            }
          });
        });
      }
      /**
       * Display an error message if conflicting options are used together in this.
       *
       * @private
       */
      _checkForConflictingLocalOptions() {
        const definedNonDefaultOptions = this.options.filter((option) => {
          const optionKey = option.attributeName();
          if (this.getOptionValue(optionKey) === void 0) {
            return false;
          }
          return this.getOptionValueSource(optionKey) !== "default";
        });
        const optionsWithConflicting = definedNonDefaultOptions.filter(
          (option) => option.conflictsWith.length > 0
        );
        optionsWithConflicting.forEach((option) => {
          const conflictingAndDefined = definedNonDefaultOptions.find(
            (defined) => option.conflictsWith.includes(defined.attributeName())
          );
          if (conflictingAndDefined) {
            this._conflictingOption(option, conflictingAndDefined);
          }
        });
      }
      /**
       * Display an error message if conflicting options are used together.
       * Called after checking for help flags in leaf subcommand.
       *
       * @private
       */
      _checkForConflictingOptions() {
        this._getCommandAndAncestors().forEach((cmd) => {
          cmd._checkForConflictingLocalOptions();
        });
      }
      /**
       * Parse options from `argv` removing known options,
       * and return argv split into operands and unknown arguments.
       *
       * Examples:
       *
       *     argv => operands, unknown
       *     --known kkk op => [op], []
       *     op --known kkk => [op], []
       *     sub --unknown uuu op => [sub], [--unknown uuu op]
       *     sub -- --unknown uuu op => [sub --unknown uuu op], []
       *
       * @param {string[]} argv
       * @return {{operands: string[], unknown: string[]}}
       */
      parseOptions(argv) {
        const operands = [];
        const unknown = [];
        let dest = operands;
        const args = argv.slice();
        function maybeOption(arg) {
          return arg.length > 1 && arg[0] === "-";
        }
        let activeVariadicOption = null;
        while (args.length) {
          const arg = args.shift();
          if (arg === "--") {
            if (dest === unknown) dest.push(arg);
            dest.push(...args);
            break;
          }
          if (activeVariadicOption && !maybeOption(arg)) {
            this.emit(`option:${activeVariadicOption.name()}`, arg);
            continue;
          }
          activeVariadicOption = null;
          if (maybeOption(arg)) {
            const option = this._findOption(arg);
            if (option) {
              if (option.required) {
                const value = args.shift();
                if (value === void 0) this.optionMissingArgument(option);
                this.emit(`option:${option.name()}`, value);
              } else if (option.optional) {
                let value = null;
                if (args.length > 0 && !maybeOption(args[0])) {
                  value = args.shift();
                }
                this.emit(`option:${option.name()}`, value);
              } else {
                this.emit(`option:${option.name()}`);
              }
              activeVariadicOption = option.variadic ? option : null;
              continue;
            }
          }
          if (arg.length > 2 && arg[0] === "-" && arg[1] !== "-") {
            const option = this._findOption(`-${arg[1]}`);
            if (option) {
              if (option.required || option.optional && this._combineFlagAndOptionalValue) {
                this.emit(`option:${option.name()}`, arg.slice(2));
              } else {
                this.emit(`option:${option.name()}`);
                args.unshift(`-${arg.slice(2)}`);
              }
              continue;
            }
          }
          if (/^--[^=]+=/.test(arg)) {
            const index = arg.indexOf("=");
            const option = this._findOption(arg.slice(0, index));
            if (option && (option.required || option.optional)) {
              this.emit(`option:${option.name()}`, arg.slice(index + 1));
              continue;
            }
          }
          if (maybeOption(arg)) {
            dest = unknown;
          }
          if ((this._enablePositionalOptions || this._passThroughOptions) && operands.length === 0 && unknown.length === 0) {
            if (this._findCommand(arg)) {
              operands.push(arg);
              if (args.length > 0) unknown.push(...args);
              break;
            } else if (this._getHelpCommand() && arg === this._getHelpCommand().name()) {
              operands.push(arg);
              if (args.length > 0) operands.push(...args);
              break;
            } else if (this._defaultCommandName) {
              unknown.push(arg);
              if (args.length > 0) unknown.push(...args);
              break;
            }
          }
          if (this._passThroughOptions) {
            dest.push(arg);
            if (args.length > 0) dest.push(...args);
            break;
          }
          dest.push(arg);
        }
        return { operands, unknown };
      }
      /**
       * Return an object containing local option values as key-value pairs.
       *
       * @return {object}
       */
      opts() {
        if (this._storeOptionsAsProperties) {
          const result = {};
          const len = this.options.length;
          for (let i = 0; i < len; i++) {
            const key = this.options[i].attributeName();
            result[key] = key === this._versionOptionName ? this._version : this[key];
          }
          return result;
        }
        return this._optionValues;
      }
      /**
       * Return an object containing merged local and global option values as key-value pairs.
       *
       * @return {object}
       */
      optsWithGlobals() {
        return this._getCommandAndAncestors().reduce(
          (combinedOptions, cmd) => Object.assign(combinedOptions, cmd.opts()),
          {}
        );
      }
      /**
       * Display error message and exit (or call exitOverride).
       *
       * @param {string} message
       * @param {object} [errorOptions]
       * @param {string} [errorOptions.code] - an id string representing the error
       * @param {number} [errorOptions.exitCode] - used with process.exit
       */
      error(message, errorOptions) {
        this._outputConfiguration.outputError(
          `${message}
`,
          this._outputConfiguration.writeErr
        );
        if (typeof this._showHelpAfterError === "string") {
          this._outputConfiguration.writeErr(`${this._showHelpAfterError}
`);
        } else if (this._showHelpAfterError) {
          this._outputConfiguration.writeErr("\n");
          this.outputHelp({ error: true });
        }
        const config = errorOptions || {};
        const exitCode = config.exitCode || 1;
        const code = config.code || "commander.error";
        this._exit(exitCode, code, message);
      }
      /**
       * Apply any option related environment variables, if option does
       * not have a value from cli or client code.
       *
       * @private
       */
      _parseOptionsEnv() {
        this.options.forEach((option) => {
          if (option.envVar && option.envVar in process8.env) {
            const optionKey = option.attributeName();
            if (this.getOptionValue(optionKey) === void 0 || ["default", "config", "env"].includes(
              this.getOptionValueSource(optionKey)
            )) {
              if (option.required || option.optional) {
                this.emit(`optionEnv:${option.name()}`, process8.env[option.envVar]);
              } else {
                this.emit(`optionEnv:${option.name()}`);
              }
            }
          }
        });
      }
      /**
       * Apply any implied option values, if option is undefined or default value.
       *
       * @private
       */
      _parseOptionsImplied() {
        const dualHelper = new DualOptions(this.options);
        const hasCustomOptionValue = (optionKey) => {
          return this.getOptionValue(optionKey) !== void 0 && !["default", "implied"].includes(this.getOptionValueSource(optionKey));
        };
        this.options.filter(
          (option) => option.implied !== void 0 && hasCustomOptionValue(option.attributeName()) && dualHelper.valueFromOption(
            this.getOptionValue(option.attributeName()),
            option
          )
        ).forEach((option) => {
          Object.keys(option.implied).filter((impliedKey) => !hasCustomOptionValue(impliedKey)).forEach((impliedKey) => {
            this.setOptionValueWithSource(
              impliedKey,
              option.implied[impliedKey],
              "implied"
            );
          });
        });
      }
      /**
       * Argument `name` is missing.
       *
       * @param {string} name
       * @private
       */
      missingArgument(name) {
        const message = `error: missing required argument '${name}'`;
        this.error(message, { code: "commander.missingArgument" });
      }
      /**
       * `Option` is missing an argument.
       *
       * @param {Option} option
       * @private
       */
      optionMissingArgument(option) {
        const message = `error: option '${option.flags}' argument missing`;
        this.error(message, { code: "commander.optionMissingArgument" });
      }
      /**
       * `Option` does not have a value, and is a mandatory option.
       *
       * @param {Option} option
       * @private
       */
      missingMandatoryOptionValue(option) {
        const message = `error: required option '${option.flags}' not specified`;
        this.error(message, { code: "commander.missingMandatoryOptionValue" });
      }
      /**
       * `Option` conflicts with another option.
       *
       * @param {Option} option
       * @param {Option} conflictingOption
       * @private
       */
      _conflictingOption(option, conflictingOption) {
        const findBestOptionFromValue = (option2) => {
          const optionKey = option2.attributeName();
          const optionValue = this.getOptionValue(optionKey);
          const negativeOption = this.options.find(
            (target) => target.negate && optionKey === target.attributeName()
          );
          const positiveOption = this.options.find(
            (target) => !target.negate && optionKey === target.attributeName()
          );
          if (negativeOption && (negativeOption.presetArg === void 0 && optionValue === false || negativeOption.presetArg !== void 0 && optionValue === negativeOption.presetArg)) {
            return negativeOption;
          }
          return positiveOption || option2;
        };
        const getErrorMessage = (option2) => {
          const bestOption = findBestOptionFromValue(option2);
          const optionKey = bestOption.attributeName();
          const source = this.getOptionValueSource(optionKey);
          if (source === "env") {
            return `environment variable '${bestOption.envVar}'`;
          }
          return `option '${bestOption.flags}'`;
        };
        const message = `error: ${getErrorMessage(option)} cannot be used with ${getErrorMessage(conflictingOption)}`;
        this.error(message, { code: "commander.conflictingOption" });
      }
      /**
       * Unknown option `flag`.
       *
       * @param {string} flag
       * @private
       */
      unknownOption(flag) {
        if (this._allowUnknownOption) return;
        let suggestion = "";
        if (flag.startsWith("--") && this._showSuggestionAfterError) {
          let candidateFlags = [];
          let command = this;
          do {
            const moreFlags = command.createHelp().visibleOptions(command).filter((option) => option.long).map((option) => option.long);
            candidateFlags = candidateFlags.concat(moreFlags);
            command = command.parent;
          } while (command && !command._enablePositionalOptions);
          suggestion = suggestSimilar(flag, candidateFlags);
        }
        const message = `error: unknown option '${flag}'${suggestion}`;
        this.error(message, { code: "commander.unknownOption" });
      }
      /**
       * Excess arguments, more than expected.
       *
       * @param {string[]} receivedArgs
       * @private
       */
      _excessArguments(receivedArgs) {
        if (this._allowExcessArguments) return;
        const expected = this.registeredArguments.length;
        const s = expected === 1 ? "" : "s";
        const forSubcommand = this.parent ? ` for '${this.name()}'` : "";
        const message = `error: too many arguments${forSubcommand}. Expected ${expected} argument${s} but got ${receivedArgs.length}.`;
        this.error(message, { code: "commander.excessArguments" });
      }
      /**
       * Unknown command.
       *
       * @private
       */
      unknownCommand() {
        const unknownName = this.args[0];
        let suggestion = "";
        if (this._showSuggestionAfterError) {
          const candidateNames = [];
          this.createHelp().visibleCommands(this).forEach((command) => {
            candidateNames.push(command.name());
            if (command.alias()) candidateNames.push(command.alias());
          });
          suggestion = suggestSimilar(unknownName, candidateNames);
        }
        const message = `error: unknown command '${unknownName}'${suggestion}`;
        this.error(message, { code: "commander.unknownCommand" });
      }
      /**
       * Get or set the program version.
       *
       * This method auto-registers the "-V, --version" option which will print the version number.
       *
       * You can optionally supply the flags and description to override the defaults.
       *
       * @param {string} [str]
       * @param {string} [flags]
       * @param {string} [description]
       * @return {(this | string | undefined)} `this` command for chaining, or version string if no arguments
       */
      version(str, flags, description) {
        if (str === void 0) return this._version;
        this._version = str;
        flags = flags || "-V, --version";
        description = description || "output the version number";
        const versionOption = this.createOption(flags, description);
        this._versionOptionName = versionOption.attributeName();
        this._registerOption(versionOption);
        this.on("option:" + versionOption.name(), () => {
          this._outputConfiguration.writeOut(`${str}
`);
          this._exit(0, "commander.version", str);
        });
        return this;
      }
      /**
       * Set the description.
       *
       * @param {string} [str]
       * @param {object} [argsDescription]
       * @return {(string|Command)}
       */
      description(str, argsDescription) {
        if (str === void 0 && argsDescription === void 0)
          return this._description;
        this._description = str;
        if (argsDescription) {
          this._argsDescription = argsDescription;
        }
        return this;
      }
      /**
       * Set the summary. Used when listed as subcommand of parent.
       *
       * @param {string} [str]
       * @return {(string|Command)}
       */
      summary(str) {
        if (str === void 0) return this._summary;
        this._summary = str;
        return this;
      }
      /**
       * Set an alias for the command.
       *
       * You may call more than once to add multiple aliases. Only the first alias is shown in the auto-generated help.
       *
       * @param {string} [alias]
       * @return {(string|Command)}
       */
      alias(alias) {
        if (alias === void 0) return this._aliases[0];
        let command = this;
        if (this.commands.length !== 0 && this.commands[this.commands.length - 1]._executableHandler) {
          command = this.commands[this.commands.length - 1];
        }
        if (alias === command._name)
          throw new Error("Command alias can't be the same as its name");
        const matchingCommand = this.parent?._findCommand(alias);
        if (matchingCommand) {
          const existingCmd = [matchingCommand.name()].concat(matchingCommand.aliases()).join("|");
          throw new Error(
            `cannot add alias '${alias}' to command '${this.name()}' as already have command '${existingCmd}'`
          );
        }
        command._aliases.push(alias);
        return this;
      }
      /**
       * Set aliases for the command.
       *
       * Only the first alias is shown in the auto-generated help.
       *
       * @param {string[]} [aliases]
       * @return {(string[]|Command)}
       */
      aliases(aliases) {
        if (aliases === void 0) return this._aliases;
        aliases.forEach((alias) => this.alias(alias));
        return this;
      }
      /**
       * Set / get the command usage `str`.
       *
       * @param {string} [str]
       * @return {(string|Command)}
       */
      usage(str) {
        if (str === void 0) {
          if (this._usage) return this._usage;
          const args = this.registeredArguments.map((arg) => {
            return humanReadableArgName(arg);
          });
          return [].concat(
            this.options.length || this._helpOption !== null ? "[options]" : [],
            this.commands.length ? "[command]" : [],
            this.registeredArguments.length ? args : []
          ).join(" ");
        }
        this._usage = str;
        return this;
      }
      /**
       * Get or set the name of the command.
       *
       * @param {string} [str]
       * @return {(string|Command)}
       */
      name(str) {
        if (str === void 0) return this._name;
        this._name = str;
        return this;
      }
      /**
       * Set the name of the command from script filename, such as process.argv[1],
       * or require.main.filename, or __filename.
       *
       * (Used internally and public although not documented in README.)
       *
       * @example
       * program.nameFromFilename(require.main.filename);
       *
       * @param {string} filename
       * @return {Command}
       */
      nameFromFilename(filename) {
        this._name = path13.basename(filename, path13.extname(filename));
        return this;
      }
      /**
       * Get or set the directory for searching for executable subcommands of this command.
       *
       * @example
       * program.executableDir(__dirname);
       * // or
       * program.executableDir('subcommands');
       *
       * @param {string} [path]
       * @return {(string|null|Command)}
       */
      executableDir(path14) {
        if (path14 === void 0) return this._executableDir;
        this._executableDir = path14;
        return this;
      }
      /**
       * Return program help documentation.
       *
       * @param {{ error: boolean }} [contextOptions] - pass {error:true} to wrap for stderr instead of stdout
       * @return {string}
       */
      helpInformation(contextOptions) {
        const helper = this.createHelp();
        if (helper.helpWidth === void 0) {
          helper.helpWidth = contextOptions && contextOptions.error ? this._outputConfiguration.getErrHelpWidth() : this._outputConfiguration.getOutHelpWidth();
        }
        return helper.formatHelp(this, helper);
      }
      /**
       * @private
       */
      _getHelpContext(contextOptions) {
        contextOptions = contextOptions || {};
        const context = { error: !!contextOptions.error };
        let write;
        if (context.error) {
          write = (arg) => this._outputConfiguration.writeErr(arg);
        } else {
          write = (arg) => this._outputConfiguration.writeOut(arg);
        }
        context.write = contextOptions.write || write;
        context.command = this;
        return context;
      }
      /**
       * Output help information for this command.
       *
       * Outputs built-in help, and custom text added using `.addHelpText()`.
       *
       * @param {{ error: boolean } | Function} [contextOptions] - pass {error:true} to write to stderr instead of stdout
       */
      outputHelp(contextOptions) {
        let deprecatedCallback;
        if (typeof contextOptions === "function") {
          deprecatedCallback = contextOptions;
          contextOptions = void 0;
        }
        const context = this._getHelpContext(contextOptions);
        this._getCommandAndAncestors().reverse().forEach((command) => command.emit("beforeAllHelp", context));
        this.emit("beforeHelp", context);
        let helpInformation = this.helpInformation(context);
        if (deprecatedCallback) {
          helpInformation = deprecatedCallback(helpInformation);
          if (typeof helpInformation !== "string" && !Buffer.isBuffer(helpInformation)) {
            throw new Error("outputHelp callback must return a string or a Buffer");
          }
        }
        context.write(helpInformation);
        if (this._getHelpOption()?.long) {
          this.emit(this._getHelpOption().long);
        }
        this.emit("afterHelp", context);
        this._getCommandAndAncestors().forEach(
          (command) => command.emit("afterAllHelp", context)
        );
      }
      /**
       * You can pass in flags and a description to customise the built-in help option.
       * Pass in false to disable the built-in help option.
       *
       * @example
       * program.helpOption('-?, --help' 'show help'); // customise
       * program.helpOption(false); // disable
       *
       * @param {(string | boolean)} flags
       * @param {string} [description]
       * @return {Command} `this` command for chaining
       */
      helpOption(flags, description) {
        if (typeof flags === "boolean") {
          if (flags) {
            this._helpOption = this._helpOption ?? void 0;
          } else {
            this._helpOption = null;
          }
          return this;
        }
        flags = flags ?? "-h, --help";
        description = description ?? "display help for command";
        this._helpOption = this.createOption(flags, description);
        return this;
      }
      /**
       * Lazy create help option.
       * Returns null if has been disabled with .helpOption(false).
       *
       * @returns {(Option | null)} the help option
       * @package
       */
      _getHelpOption() {
        if (this._helpOption === void 0) {
          this.helpOption(void 0, void 0);
        }
        return this._helpOption;
      }
      /**
       * Supply your own option to use for the built-in help option.
       * This is an alternative to using helpOption() to customise the flags and description etc.
       *
       * @param {Option} option
       * @return {Command} `this` command for chaining
       */
      addHelpOption(option) {
        this._helpOption = option;
        return this;
      }
      /**
       * Output help information and exit.
       *
       * Outputs built-in help, and custom text added using `.addHelpText()`.
       *
       * @param {{ error: boolean }} [contextOptions] - pass {error:true} to write to stderr instead of stdout
       */
      help(contextOptions) {
        this.outputHelp(contextOptions);
        let exitCode = process8.exitCode || 0;
        if (exitCode === 0 && contextOptions && typeof contextOptions !== "function" && contextOptions.error) {
          exitCode = 1;
        }
        this._exit(exitCode, "commander.help", "(outputHelp)");
      }
      /**
       * Add additional text to be displayed with the built-in help.
       *
       * Position is 'before' or 'after' to affect just this command,
       * and 'beforeAll' or 'afterAll' to affect this command and all its subcommands.
       *
       * @param {string} position - before or after built-in help
       * @param {(string | Function)} text - string to add, or a function returning a string
       * @return {Command} `this` command for chaining
       */
      addHelpText(position, text2) {
        const allowedValues = ["beforeAll", "before", "after", "afterAll"];
        if (!allowedValues.includes(position)) {
          throw new Error(`Unexpected value for position to addHelpText.
Expecting one of '${allowedValues.join("', '")}'`);
        }
        const helpEvent = `${position}Help`;
        this.on(helpEvent, (context) => {
          let helpStr;
          if (typeof text2 === "function") {
            helpStr = text2({ error: context.error, command: context.command });
          } else {
            helpStr = text2;
          }
          if (helpStr) {
            context.write(`${helpStr}
`);
          }
        });
        return this;
      }
      /**
       * Output help information if help flags specified
       *
       * @param {Array} args - array of options to search for help flags
       * @private
       */
      _outputHelpIfRequested(args) {
        const helpOption = this._getHelpOption();
        const helpRequested = helpOption && args.find((arg) => helpOption.is(arg));
        if (helpRequested) {
          this.outputHelp();
          this._exit(0, "commander.helpDisplayed", "(outputHelp)");
        }
      }
    };
    function incrementNodeInspectorPort(args) {
      return args.map((arg) => {
        if (!arg.startsWith("--inspect")) {
          return arg;
        }
        let debugOption;
        let debugHost = "127.0.0.1";
        let debugPort = "9229";
        let match;
        if ((match = arg.match(/^(--inspect(-brk)?)$/)) !== null) {
          debugOption = match[1];
        } else if ((match = arg.match(/^(--inspect(-brk|-port)?)=([^:]+)$/)) !== null) {
          debugOption = match[1];
          if (/^\d+$/.test(match[3])) {
            debugPort = match[3];
          } else {
            debugHost = match[3];
          }
        } else if ((match = arg.match(/^(--inspect(-brk|-port)?)=([^:]+):(\d+)$/)) !== null) {
          debugOption = match[1];
          debugHost = match[3];
          debugPort = match[4];
        }
        if (debugOption && debugPort !== "0") {
          return `${debugOption}=${debugHost}:${parseInt(debugPort) + 1}`;
        }
        return arg;
      });
    }
    exports2.Command = Command2;
  }
});

// node_modules/.pnpm/commander@12.1.0/node_modules/commander/index.js
var require_commander = __commonJS({
  "node_modules/.pnpm/commander@12.1.0/node_modules/commander/index.js"(exports2) {
    var { Argument: Argument2 } = require_argument();
    var { Command: Command2 } = require_command();
    var { CommanderError: CommanderError2, InvalidArgumentError: InvalidArgumentError2 } = require_error();
    var { Help: Help2 } = require_help();
    var { Option: Option2 } = require_option();
    exports2.program = new Command2();
    exports2.createCommand = (name) => new Command2(name);
    exports2.createOption = (flags, description) => new Option2(flags, description);
    exports2.createArgument = (name, description) => new Argument2(name, description);
    exports2.Command = Command2;
    exports2.Option = Option2;
    exports2.Argument = Argument2;
    exports2.Help = Help2;
    exports2.CommanderError = CommanderError2;
    exports2.InvalidArgumentError = InvalidArgumentError2;
    exports2.InvalidOptionArgumentError = InvalidArgumentError2;
  }
});

// node_modules/.pnpm/is-docker@3.0.0/node_modules/is-docker/index.js
function hasDockerEnv() {
  try {
    import_node_fs.default.statSync("/.dockerenv");
    return true;
  } catch {
    return false;
  }
}
function hasDockerCGroup() {
  try {
    return import_node_fs.default.readFileSync("/proc/self/cgroup", "utf8").includes("docker");
  } catch {
    return false;
  }
}
function isDocker() {
  if (isDockerCached === void 0) {
    isDockerCached = hasDockerEnv() || hasDockerCGroup();
  }
  return isDockerCached;
}
var import_node_fs, isDockerCached;
var init_is_docker = __esm({
  "node_modules/.pnpm/is-docker@3.0.0/node_modules/is-docker/index.js"() {
    import_node_fs = __toESM(require("node:fs"), 1);
  }
});

// node_modules/.pnpm/is-inside-container@1.0.0/node_modules/is-inside-container/index.js
function isInsideContainer() {
  if (cachedResult === void 0) {
    cachedResult = hasContainerEnv() || isDocker();
  }
  return cachedResult;
}
var import_node_fs2, cachedResult, hasContainerEnv;
var init_is_inside_container = __esm({
  "node_modules/.pnpm/is-inside-container@1.0.0/node_modules/is-inside-container/index.js"() {
    import_node_fs2 = __toESM(require("node:fs"), 1);
    init_is_docker();
    hasContainerEnv = () => {
      try {
        import_node_fs2.default.statSync("/run/.containerenv");
        return true;
      } catch {
        return false;
      }
    };
  }
});

// node_modules/.pnpm/is-wsl@3.1.1/node_modules/is-wsl/index.js
var import_node_process, import_node_os, import_node_fs3, isWsl, is_wsl_default;
var init_is_wsl = __esm({
  "node_modules/.pnpm/is-wsl@3.1.1/node_modules/is-wsl/index.js"() {
    import_node_process = __toESM(require("node:process"), 1);
    import_node_os = __toESM(require("node:os"), 1);
    import_node_fs3 = __toESM(require("node:fs"), 1);
    init_is_inside_container();
    isWsl = () => {
      if (import_node_process.default.platform !== "linux") {
        return false;
      }
      if (import_node_os.default.release().toLowerCase().includes("microsoft")) {
        if (isInsideContainer()) {
          return false;
        }
        return true;
      }
      try {
        if (import_node_fs3.default.readFileSync("/proc/version", "utf8").toLowerCase().includes("microsoft")) {
          return !isInsideContainer();
        }
      } catch {
      }
      if (import_node_fs3.default.existsSync("/proc/sys/fs/binfmt_misc/WSLInterop") || import_node_fs3.default.existsSync("/run/WSL")) {
        return !isInsideContainer();
      }
      return false;
    };
    is_wsl_default = import_node_process.default.env.__IS_WSL_TEST__ ? isWsl : isWsl();
  }
});

// node_modules/.pnpm/wsl-utils@0.1.0/node_modules/wsl-utils/index.js
var import_node_process2, import_promises, wslDrivesMountPoint, powerShellPathFromWsl, powerShellPath;
var init_wsl_utils = __esm({
  "node_modules/.pnpm/wsl-utils@0.1.0/node_modules/wsl-utils/index.js"() {
    import_node_process2 = __toESM(require("node:process"), 1);
    import_promises = __toESM(require("node:fs/promises"), 1);
    init_is_wsl();
    init_is_wsl();
    wslDrivesMountPoint = /* @__PURE__ */ (() => {
      const defaultMountPoint = "/mnt/";
      let mountPoint;
      return async function() {
        if (mountPoint) {
          return mountPoint;
        }
        const configFilePath2 = "/etc/wsl.conf";
        let isConfigFileExists = false;
        try {
          await import_promises.default.access(configFilePath2, import_promises.constants.F_OK);
          isConfigFileExists = true;
        } catch {
        }
        if (!isConfigFileExists) {
          return defaultMountPoint;
        }
        const configContent = await import_promises.default.readFile(configFilePath2, { encoding: "utf8" });
        const configMountPoint = /(?<!#.*)root\s*=\s*(?<mountPoint>.*)/g.exec(configContent);
        if (!configMountPoint) {
          return defaultMountPoint;
        }
        mountPoint = configMountPoint.groups.mountPoint.trim();
        mountPoint = mountPoint.endsWith("/") ? mountPoint : `${mountPoint}/`;
        return mountPoint;
      };
    })();
    powerShellPathFromWsl = async () => {
      const mountPoint = await wslDrivesMountPoint();
      return `${mountPoint}c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`;
    };
    powerShellPath = async () => {
      if (is_wsl_default) {
        return powerShellPathFromWsl();
      }
      return `${import_node_process2.default.env.SYSTEMROOT || import_node_process2.default.env.windir || String.raw`C:\Windows`}\\System32\\WindowsPowerShell\\v1.0\\powershell.exe`;
    };
  }
});

// node_modules/.pnpm/define-lazy-prop@3.0.0/node_modules/define-lazy-prop/index.js
function defineLazyProperty(object, propertyName, valueGetter) {
  const define = (value) => Object.defineProperty(object, propertyName, { value, enumerable: true, writable: true });
  Object.defineProperty(object, propertyName, {
    configurable: true,
    enumerable: true,
    get() {
      const result = valueGetter();
      define(result);
      return result;
    },
    set(value) {
      define(value);
    }
  });
  return object;
}
var init_define_lazy_prop = __esm({
  "node_modules/.pnpm/define-lazy-prop@3.0.0/node_modules/define-lazy-prop/index.js"() {
  }
});

// node_modules/.pnpm/default-browser-id@5.0.1/node_modules/default-browser-id/index.js
async function defaultBrowserId() {
  if (import_node_process3.default.platform !== "darwin") {
    throw new Error("macOS only");
  }
  const { stdout } = await execFileAsync("defaults", ["read", "com.apple.LaunchServices/com.apple.launchservices.secure", "LSHandlers"]);
  const match = /LSHandlerRoleAll = "(?!-)(?<id>[^"]+?)";\s+?LSHandlerURLScheme = (?:http|https);/.exec(stdout);
  const browserId = match?.groups.id ?? "com.apple.Safari";
  if (browserId === "com.apple.safari") {
    return "com.apple.Safari";
  }
  return browserId;
}
var import_node_util, import_node_process3, import_node_child_process, execFileAsync;
var init_default_browser_id = __esm({
  "node_modules/.pnpm/default-browser-id@5.0.1/node_modules/default-browser-id/index.js"() {
    import_node_util = require("node:util");
    import_node_process3 = __toESM(require("node:process"), 1);
    import_node_child_process = require("node:child_process");
    execFileAsync = (0, import_node_util.promisify)(import_node_child_process.execFile);
  }
});

// node_modules/.pnpm/run-applescript@7.1.0/node_modules/run-applescript/index.js
async function runAppleScript(script, { humanReadableOutput = true, signal } = {}) {
  if (import_node_process4.default.platform !== "darwin") {
    throw new Error("macOS only");
  }
  const outputArguments = humanReadableOutput ? [] : ["-ss"];
  const execOptions = {};
  if (signal) {
    execOptions.signal = signal;
  }
  const { stdout } = await execFileAsync2("osascript", ["-e", script, outputArguments], execOptions);
  return stdout.trim();
}
var import_node_process4, import_node_util2, import_node_child_process2, execFileAsync2;
var init_run_applescript = __esm({
  "node_modules/.pnpm/run-applescript@7.1.0/node_modules/run-applescript/index.js"() {
    import_node_process4 = __toESM(require("node:process"), 1);
    import_node_util2 = require("node:util");
    import_node_child_process2 = require("node:child_process");
    execFileAsync2 = (0, import_node_util2.promisify)(import_node_child_process2.execFile);
  }
});

// node_modules/.pnpm/bundle-name@4.1.0/node_modules/bundle-name/index.js
async function bundleName(bundleId) {
  return runAppleScript(`tell application "Finder" to set app_path to application file id "${bundleId}" as string
tell application "System Events" to get value of property list item "CFBundleName" of property list file (app_path & ":Contents:Info.plist")`);
}
var init_bundle_name = __esm({
  "node_modules/.pnpm/bundle-name@4.1.0/node_modules/bundle-name/index.js"() {
    init_run_applescript();
  }
});

// node_modules/.pnpm/default-browser@5.5.0/node_modules/default-browser/windows.js
async function defaultBrowser(_execFileAsync = execFileAsync3) {
  const { stdout } = await _execFileAsync("reg", [
    "QUERY",
    " HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice",
    "/v",
    "ProgId"
  ]);
  const match = /ProgId\s*REG_SZ\s*(?<id>\S+)/.exec(stdout);
  if (!match) {
    throw new UnknownBrowserError(`Cannot find Windows browser in stdout: ${JSON.stringify(stdout)}`);
  }
  const { id } = match.groups;
  const dotIndex = id.lastIndexOf(".");
  const hyphenIndex = id.lastIndexOf("-");
  const baseIdByDot = dotIndex === -1 ? void 0 : id.slice(0, dotIndex);
  const baseIdByHyphen = hyphenIndex === -1 ? void 0 : id.slice(0, hyphenIndex);
  return windowsBrowserProgIds[id] ?? windowsBrowserProgIds[baseIdByDot] ?? windowsBrowserProgIds[baseIdByHyphen] ?? { name: id, id };
}
var import_node_util3, import_node_child_process3, execFileAsync3, windowsBrowserProgIds, _windowsBrowserProgIdMap, UnknownBrowserError;
var init_windows = __esm({
  "node_modules/.pnpm/default-browser@5.5.0/node_modules/default-browser/windows.js"() {
    import_node_util3 = require("node:util");
    import_node_child_process3 = require("node:child_process");
    execFileAsync3 = (0, import_node_util3.promisify)(import_node_child_process3.execFile);
    windowsBrowserProgIds = {
      MSEdgeHTM: { name: "Edge", id: "com.microsoft.edge" },
      // The missing `L` is correct.
      MSEdgeBHTML: { name: "Edge Beta", id: "com.microsoft.edge.beta" },
      MSEdgeDHTML: { name: "Edge Dev", id: "com.microsoft.edge.dev" },
      AppXq0fevzme2pys62n3e0fbqa7peapykr8v: { name: "Edge", id: "com.microsoft.edge.old" },
      ChromeHTML: { name: "Chrome", id: "com.google.chrome" },
      ChromeBHTML: { name: "Chrome Beta", id: "com.google.chrome.beta" },
      ChromeDHTML: { name: "Chrome Dev", id: "com.google.chrome.dev" },
      ChromiumHTM: { name: "Chromium", id: "org.chromium.Chromium" },
      BraveHTML: { name: "Brave", id: "com.brave.Browser" },
      BraveBHTML: { name: "Brave Beta", id: "com.brave.Browser.beta" },
      BraveDHTML: { name: "Brave Dev", id: "com.brave.Browser.dev" },
      BraveSSHTM: { name: "Brave Nightly", id: "com.brave.Browser.nightly" },
      FirefoxURL: { name: "Firefox", id: "org.mozilla.firefox" },
      OperaStable: { name: "Opera", id: "com.operasoftware.Opera" },
      VivaldiHTM: { name: "Vivaldi", id: "com.vivaldi.Vivaldi" },
      "IE.HTTP": { name: "Internet Explorer", id: "com.microsoft.ie" }
    };
    _windowsBrowserProgIdMap = new Map(Object.entries(windowsBrowserProgIds));
    UnknownBrowserError = class extends Error {
    };
  }
});

// node_modules/.pnpm/default-browser@5.5.0/node_modules/default-browser/index.js
async function defaultBrowser2() {
  if (import_node_process5.default.platform === "darwin") {
    const id = await defaultBrowserId();
    const name = await bundleName(id);
    return { name, id };
  }
  if (import_node_process5.default.platform === "linux") {
    const { stdout } = await execFileAsync4("xdg-mime", ["query", "default", "x-scheme-handler/http"]);
    const id = stdout.trim();
    const name = titleize(id.replace(/.desktop$/, "").replace("-", " "));
    return { name, id };
  }
  if (import_node_process5.default.platform === "win32") {
    return defaultBrowser();
  }
  throw new Error("Only macOS, Linux, and Windows are supported");
}
var import_node_util4, import_node_process5, import_node_child_process4, execFileAsync4, titleize;
var init_default_browser = __esm({
  "node_modules/.pnpm/default-browser@5.5.0/node_modules/default-browser/index.js"() {
    import_node_util4 = require("node:util");
    import_node_process5 = __toESM(require("node:process"), 1);
    import_node_child_process4 = require("node:child_process");
    init_default_browser_id();
    init_bundle_name();
    init_windows();
    execFileAsync4 = (0, import_node_util4.promisify)(import_node_child_process4.execFile);
    titleize = (string) => string.toLowerCase().replaceAll(/(?:^|\s|-)\S/g, (x) => x.toUpperCase());
  }
});

// node_modules/.pnpm/open@10.2.0/node_modules/open/index.js
var open_exports = {};
__export(open_exports, {
  apps: () => apps,
  default: () => open_default,
  openApp: () => openApp
});
async function getWindowsDefaultBrowserFromWsl() {
  const powershellPath = await powerShellPath();
  const rawCommand = String.raw`(Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice").ProgId`;
  const encodedCommand = import_node_buffer.Buffer.from(rawCommand, "utf16le").toString("base64");
  const { stdout } = await execFile5(
    powershellPath,
    [
      "-NoProfile",
      "-NonInteractive",
      "-ExecutionPolicy",
      "Bypass",
      "-EncodedCommand",
      encodedCommand
    ],
    { encoding: "utf8" }
  );
  const progId = stdout.trim();
  const browserMap = {
    ChromeHTML: "com.google.chrome",
    BraveHTML: "com.brave.Browser",
    MSEdgeHTM: "com.microsoft.edge",
    FirefoxURL: "org.mozilla.firefox"
  };
  return browserMap[progId] ? { id: browserMap[progId] } : {};
}
function detectArchBinary(binary) {
  if (typeof binary === "string" || Array.isArray(binary)) {
    return binary;
  }
  const { [arch]: archBinary } = binary;
  if (!archBinary) {
    throw new Error(`${arch} is not supported`);
  }
  return archBinary;
}
function detectPlatformBinary({ [platform]: platformBinary }, { wsl }) {
  if (wsl && is_wsl_default) {
    return detectArchBinary(wsl);
  }
  if (!platformBinary) {
    throw new Error(`${platform} is not supported`);
  }
  return detectArchBinary(platformBinary);
}
var import_node_process6, import_node_buffer, import_node_path, import_node_url, import_node_util5, import_node_child_process5, import_promises2, import_meta, execFile5, __dirname2, localXdgOpenPath, platform, arch, pTryEach, baseOpen, open, openApp, apps, open_default;
var init_open = __esm({
  "node_modules/.pnpm/open@10.2.0/node_modules/open/index.js"() {
    import_node_process6 = __toESM(require("node:process"), 1);
    import_node_buffer = require("node:buffer");
    import_node_path = __toESM(require("node:path"), 1);
    import_node_url = require("node:url");
    import_node_util5 = require("node:util");
    import_node_child_process5 = __toESM(require("node:child_process"), 1);
    import_promises2 = __toESM(require("node:fs/promises"), 1);
    init_wsl_utils();
    init_define_lazy_prop();
    init_default_browser();
    init_is_inside_container();
    import_meta = {};
    execFile5 = (0, import_node_util5.promisify)(import_node_child_process5.default.execFile);
    __dirname2 = import_node_path.default.dirname((0, import_node_url.fileURLToPath)(import_meta.url));
    localXdgOpenPath = import_node_path.default.join(__dirname2, "xdg-open");
    ({ platform, arch } = import_node_process6.default);
    pTryEach = async (array, mapper) => {
      let latestError;
      for (const item of array) {
        try {
          return await mapper(item);
        } catch (error) {
          latestError = error;
        }
      }
      throw latestError;
    };
    baseOpen = async (options) => {
      options = {
        wait: false,
        background: false,
        newInstance: false,
        allowNonzeroExitCode: false,
        ...options
      };
      if (Array.isArray(options.app)) {
        return pTryEach(options.app, (singleApp) => baseOpen({
          ...options,
          app: singleApp
        }));
      }
      let { name: app, arguments: appArguments = [] } = options.app ?? {};
      appArguments = [...appArguments];
      if (Array.isArray(app)) {
        return pTryEach(app, (appName) => baseOpen({
          ...options,
          app: {
            name: appName,
            arguments: appArguments
          }
        }));
      }
      if (app === "browser" || app === "browserPrivate") {
        const ids = {
          "com.google.chrome": "chrome",
          "google-chrome.desktop": "chrome",
          "com.brave.Browser": "brave",
          "org.mozilla.firefox": "firefox",
          "firefox.desktop": "firefox",
          "com.microsoft.msedge": "edge",
          "com.microsoft.edge": "edge",
          "com.microsoft.edgemac": "edge",
          "microsoft-edge.desktop": "edge"
        };
        const flags = {
          chrome: "--incognito",
          brave: "--incognito",
          firefox: "--private-window",
          edge: "--inPrivate"
        };
        const browser = is_wsl_default ? await getWindowsDefaultBrowserFromWsl() : await defaultBrowser2();
        if (browser.id in ids) {
          const browserName = ids[browser.id];
          if (app === "browserPrivate") {
            appArguments.push(flags[browserName]);
          }
          return baseOpen({
            ...options,
            app: {
              name: apps[browserName],
              arguments: appArguments
            }
          });
        }
        throw new Error(`${browser.name} is not supported as a default browser`);
      }
      let command;
      const cliArguments = [];
      const childProcessOptions = {};
      if (platform === "darwin") {
        command = "open";
        if (options.wait) {
          cliArguments.push("--wait-apps");
        }
        if (options.background) {
          cliArguments.push("--background");
        }
        if (options.newInstance) {
          cliArguments.push("--new");
        }
        if (app) {
          cliArguments.push("-a", app);
        }
      } else if (platform === "win32" || is_wsl_default && !isInsideContainer() && !app) {
        command = await powerShellPath();
        cliArguments.push(
          "-NoProfile",
          "-NonInteractive",
          "-ExecutionPolicy",
          "Bypass",
          "-EncodedCommand"
        );
        if (!is_wsl_default) {
          childProcessOptions.windowsVerbatimArguments = true;
        }
        const encodedArguments = ["Start"];
        if (options.wait) {
          encodedArguments.push("-Wait");
        }
        if (app) {
          encodedArguments.push(`"\`"${app}\`""`);
          if (options.target) {
            appArguments.push(options.target);
          }
        } else if (options.target) {
          encodedArguments.push(`"${options.target}"`);
        }
        if (appArguments.length > 0) {
          appArguments = appArguments.map((argument) => `"\`"${argument}\`""`);
          encodedArguments.push("-ArgumentList", appArguments.join(","));
        }
        options.target = import_node_buffer.Buffer.from(encodedArguments.join(" "), "utf16le").toString("base64");
      } else {
        if (app) {
          command = app;
        } else {
          const isBundled = !__dirname2 || __dirname2 === "/";
          let exeLocalXdgOpen = false;
          try {
            await import_promises2.default.access(localXdgOpenPath, import_promises2.constants.X_OK);
            exeLocalXdgOpen = true;
          } catch {
          }
          const useSystemXdgOpen = import_node_process6.default.versions.electron ?? (platform === "android" || isBundled || !exeLocalXdgOpen);
          command = useSystemXdgOpen ? "xdg-open" : localXdgOpenPath;
        }
        if (appArguments.length > 0) {
          cliArguments.push(...appArguments);
        }
        if (!options.wait) {
          childProcessOptions.stdio = "ignore";
          childProcessOptions.detached = true;
        }
      }
      if (platform === "darwin" && appArguments.length > 0) {
        cliArguments.push("--args", ...appArguments);
      }
      if (options.target) {
        cliArguments.push(options.target);
      }
      const subprocess = import_node_child_process5.default.spawn(command, cliArguments, childProcessOptions);
      if (options.wait) {
        return new Promise((resolve, reject) => {
          subprocess.once("error", reject);
          subprocess.once("close", (exitCode) => {
            if (!options.allowNonzeroExitCode && exitCode > 0) {
              reject(new Error(`Exited with code ${exitCode}`));
              return;
            }
            resolve(subprocess);
          });
        });
      }
      subprocess.unref();
      return subprocess;
    };
    open = (target, options) => {
      if (typeof target !== "string") {
        throw new TypeError("Expected a `target`");
      }
      return baseOpen({
        ...options,
        target
      });
    };
    openApp = (name, options) => {
      if (typeof name !== "string" && !Array.isArray(name)) {
        throw new TypeError("Expected a valid `name`");
      }
      const { arguments: appArguments = [] } = options ?? {};
      if (appArguments !== void 0 && appArguments !== null && !Array.isArray(appArguments)) {
        throw new TypeError("Expected `appArguments` as Array type");
      }
      return baseOpen({
        ...options,
        app: {
          name,
          arguments: appArguments
        }
      });
    };
    apps = {};
    defineLazyProperty(apps, "chrome", () => detectPlatformBinary({
      darwin: "google chrome",
      win32: "chrome",
      linux: ["google-chrome", "google-chrome-stable", "chromium"]
    }, {
      wsl: {
        ia32: "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        x64: ["/mnt/c/Program Files/Google/Chrome/Application/chrome.exe", "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"]
      }
    }));
    defineLazyProperty(apps, "brave", () => detectPlatformBinary({
      darwin: "brave browser",
      win32: "brave",
      linux: ["brave-browser", "brave"]
    }, {
      wsl: {
        ia32: "/mnt/c/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe",
        x64: ["/mnt/c/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe", "/mnt/c/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe"]
      }
    }));
    defineLazyProperty(apps, "firefox", () => detectPlatformBinary({
      darwin: "firefox",
      win32: String.raw`C:\Program Files\Mozilla Firefox\firefox.exe`,
      linux: "firefox"
    }, {
      wsl: "/mnt/c/Program Files/Mozilla Firefox/firefox.exe"
    }));
    defineLazyProperty(apps, "edge", () => detectPlatformBinary({
      darwin: "microsoft edge",
      win32: "msedge",
      linux: ["microsoft-edge", "microsoft-edge-dev"]
    }, {
      wsl: "/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
    }));
    defineLazyProperty(apps, "browser", () => "browser");
    defineLazyProperty(apps, "browserPrivate", () => "browserPrivate");
    open_default = open;
  }
});

// node_modules/.pnpm/commander@12.1.0/node_modules/commander/esm.mjs
var import_index = __toESM(require_commander(), 1);
var {
  program,
  createCommand,
  createArgument,
  createOption,
  CommanderError,
  InvalidArgumentError,
  InvalidOptionArgumentError,
  // deprecated old name
  Command,
  Argument,
  Option,
  Help
} = import_index.default;

// cli/dazi/src/commands/auth.ts
var import_os3 = __toESM(require("os"), 1);
var import_path4 = __toESM(require("path"), 1);
var import_fs3 = __toESM(require("fs"), 1);

// cli/shared/src/auth.ts
var import_os = __toESM(require("os"), 1);
var import_path = __toESM(require("path"), 1);
var import_fs = __toESM(require("fs"), 1);

// cli/shared/src/errors.ts
var DaziError = class extends Error {
  constructor(message, code = "ERR_DAZI", exitCode = 1) {
    super(message);
    this.code = code;
    this.exitCode = exitCode;
    this.name = "DaziError";
  }
};
var AuthError = class extends DaziError {
  constructor(message = "\u672A\u767B\u5F55\uFF0C\u8BF7\u5148\u8FD0\u884C: dazi auth login") {
    super(message, "ERR_AUTH", 2);
    this.name = "AuthError";
  }
};
var NetworkError = class extends DaziError {
  constructor(message, status) {
    super(message, "ERR_NETWORK", 3);
    this.status = status;
    this.name = "NetworkError";
  }
};

// cli/shared/src/auth.ts
function authFilePath() {
  return import_path.default.join(import_os.default.homedir(), ".dazi", "auth.json");
}
function loadAuth() {
  const p = authFilePath();
  if (!import_fs.default.existsSync(p)) throw new AuthError();
  try {
    return JSON.parse(import_fs.default.readFileSync(p, "utf-8"));
  } catch {
    throw new AuthError("auth.json \u683C\u5F0F\u635F\u574F\uFF0C\u8BF7\u91CD\u65B0\u767B\u5F55");
  }
}
function saveAuth(data) {
  const dir = import_path.default.dirname(authFilePath());
  if (!import_fs.default.existsSync(dir)) import_fs.default.mkdirSync(dir, { recursive: true });
  import_fs.default.writeFileSync(authFilePath(), JSON.stringify(data, null, 2), "utf-8");
}
function clearAuth() {
  const p = authFilePath();
  if (import_fs.default.existsSync(p)) import_fs.default.unlinkSync(p);
}
function tryLoadAuth() {
  try {
    return loadAuth();
  } catch {
    return null;
  }
}

// cli/shared/src/httpClient.ts
async function apiRequest(path13, opts = {}) {
  const auth = opts.token || opts.serverUrl ? { token: opts.token ?? "", serverUrl: opts.serverUrl ?? "" } : loadAuth();
  const url = `${auth.serverUrl.replace(/\/$/, "")}${path13}`;
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${auth.token}`,
    ...opts.headers
  };
  const res = await fetch(url, {
    method: opts.method ?? "GET",
    headers,
    body: opts.body != null ? JSON.stringify(opts.body) : void 0
  });
  if (!res.ok) {
    let msg = `HTTP ${res.status} ${res.statusText}`;
    try {
      const j = await res.json();
      if (j.message) msg = j.message;
    } catch {
    }
    throw new NetworkError(msg, res.status);
  }
  return res.json();
}

// cli/shared/src/output.ts
function printJsonSummary(summary) {
  console.log(`__JSON_SUMMARY__${JSON.stringify(summary)}`);
}
function ok(data) {
  printJsonSummary({ ok: true, data });
}
function fail(code, message) {
  printJsonSummary({ ok: false, error: { code, message } });
}
function handleError(err2) {
  if (err2 instanceof Error) {
    const code = err2.code ?? "ERR_UNKNOWN";
    console.error(`\u9519\u8BEF: ${err2.message}`);
    fail(code, err2.message);
  } else {
    console.error(`\u672A\u77E5\u9519\u8BEF`, err2);
    fail("ERR_UNKNOWN", String(err2));
  }
  process.exit(1);
}

// cli/shared/src/config.ts
var import_os2 = __toESM(require("os"), 1);
var import_path2 = __toESM(require("path"), 1);
var import_fs2 = __toESM(require("fs"), 1);
function configFilePath() {
  return import_path2.default.join(import_os2.default.homedir(), ".dazi", "config.json");
}
function loadConfig() {
  const p = configFilePath();
  if (!import_fs2.default.existsSync(p)) return {};
  try {
    return JSON.parse(import_fs2.default.readFileSync(p, "utf-8"));
  } catch {
    return {};
  }
}
function getServerUrl() {
  return loadConfig().serverUrl ?? process.env.DAZI_SERVER_URL ?? "https://api.dazi.tech";
}

// cli/shared/src/workspaceLayout.ts
var import_path3 = __toESM(require("path"), 1);
var WORKSPACE_RESOURCE_DIR = "\u8D44\u6E90";
function resolveWorkspace(cwd = process.cwd()) {
  const resources = import_path3.default.join(cwd, WORKSPACE_RESOURCE_DIR);
  return {
    root: cwd,
    resources,
    dazi: import_path3.default.join(cwd, ".dazi"),
    onto: import_path3.default.join(cwd, "onto"),
    flows: import_path3.default.join(cwd, "flows"),
    apps: import_path3.default.join(cwd, "apps"),
    data: import_path3.default.join(cwd, "data"),
    docs: import_path3.default.join(resources, "docs"),
    prompts: import_path3.default.join(resources, "prompts"),
    examples: import_path3.default.join(resources, "examples"),
    dataspaces: import_path3.default.join(resources, "dataspaces"),
    datasources: import_path3.default.join(resources, "datasources")
  };
}

// cli/dazi/src/commands/auth.ts
function makeAuthCommand() {
  const cmd = new Command("auth").description("\u8D26\u53F7\u8BA4\u8BC1");
  cmd.command("login").description("\u767B\u5F55\u642D\u5B50\u5E73\u53F0").option("-s, --server <url>", "\u5E73\u53F0\u5730\u5740", getServerUrl()).option("--token <token>", "\u76F4\u63A5\u4F7F\u7528 token \u767B\u5F55\uFF08CI / Token \u6A21\u5F0F\uFF09").option("-u, --username <username>", "\u7528\u6237\u540D\u6216\u90AE\u7BB1\uFF08\u8D26\u53F7\u5BC6\u7801\u6A21\u5F0F\uFF09").option("-p, --password <password>", "\u5BC6\u7801\uFF08\u8D26\u53F7\u5BC6\u7801\u6A21\u5F0F\uFF09").action(async (opts) => {
    try {
      if (opts.token) {
        const user = await apiRequest(
          "/api/auth/me",
          { token: opts.token, serverUrl: opts.server }
        );
        saveAuth({
          token: opts.token,
          userId: user.id,
          username: user.username,
          email: user.email,
          serverUrl: opts.server,
          loginAt: (/* @__PURE__ */ new Date()).toISOString()
        });
        console.log(`\u2705 \u767B\u5F55\u6210\u529F: ${user.username}`);
        ok({ username: user.username, userId: user.id });
      } else if (opts.username && opts.password) {
        const resp = await apiRequest(
          "/api/auth/login",
          {
            serverUrl: opts.server,
            token: "",
            method: "POST",
            body: { username: opts.username, password: opts.password }
          }
        );
        saveAuth({
          token: resp.tokens.access_token,
          userId: resp.user.id,
          username: resp.user.username,
          email: resp.user.email,
          serverUrl: opts.server,
          loginAt: (/* @__PURE__ */ new Date()).toISOString()
        });
        console.log(`\u2705 \u767B\u5F55\u6210\u529F: ${resp.user.username}`);
        ok({ username: resp.user.username, userId: resp.user.id });
      } else {
        const loginUrl = `${opts.server.replace(/\/$/, "")}/cli-login`;
        console.log(`\u{1F310} \u6B63\u5728\u6253\u5F00\u767B\u5F55\u9875\u9762: ${loginUrl}`);
        const { default: open2 } = await Promise.resolve().then(() => (init_open(), open_exports));
        await open2(loginUrl);
        console.log("\u767B\u5F55\u5B8C\u6210\u540E\uFF0C\u8BF7\u4F7F\u7528 --token <token> \u91CD\u65B0\u8FD0\u884C\u6B64\u547D\u4EE4\u5B8C\u6210\u7ED1\u5B9A");
        ok({ loginUrl });
      }
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("logout").description("\u9000\u51FA\u767B\u5F55").action(() => {
    clearAuth();
    console.log("\u5DF2\u9000\u51FA\u767B\u5F55");
    ok({ loggedOut: true });
  });
  cmd.command("whoami").description("\u67E5\u770B\u5F53\u524D\u767B\u5F55\u8D26\u53F7").action(() => {
    const auth = tryLoadAuth();
    if (!auth) {
      console.log("\u672A\u767B\u5F55");
      fail("ERR_AUTH", "\u672A\u767B\u5F55\uFF0C\u8BF7\u5148\u8FD0\u884C: dazi auth login");
      process.exit(2);
    }
    console.log(`\u7528\u6237: ${auth.username}`);
    console.log(`\u90AE\u7BB1: ${auth.email ?? "\u2014"}`);
    console.log(`\u670D\u52A1: ${auth.serverUrl}`);
    console.log(`\u767B\u5F55: ${auth.loginAt}`);
    ok({ username: auth.username, userId: auth.userId, email: auth.email, serverUrl: auth.serverUrl });
  });
  cmd.command("set-token <token>").description("\u76F4\u63A5\u7ED1\u5B9A API Token\uFF08CI / \u811A\u672C\u573A\u666F\uFF09").option("-s, --server <url>", "\u5E73\u53F0\u5730\u5740", getServerUrl()).action(async (token, opts) => {
    try {
      const user = await apiRequest(
        "/api/auth/me",
        { token, serverUrl: opts.server }
      );
      saveAuth({ token, userId: user.id, username: user.username, email: user.email, serverUrl: opts.server, loginAt: (/* @__PURE__ */ new Date()).toISOString() });
      console.log(`\u2705 Token \u5DF2\u7ED1\u5B9A: ${user.username}`);
      ok({ username: user.username, userId: user.id });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("migrate").description("\u5C06\u65E7\u7248\u8BA4\u8BC1\u6587\u4EF6\u8FC1\u79FB\u5230 ~/.dazi/auth.json").option("--dry-run", "\u4EC5\u9884\u89C8\uFF0C\u4E0D\u5199\u5165").action(async (opts) => {
    const candidates = [];
    const appAuth = import_path4.default.join(import_os3.default.homedir(), ".dazi-app", "auth.json");
    if (import_fs3.default.existsSync(appAuth)) {
      try {
        const d = JSON.parse(import_fs3.default.readFileSync(appAuth, "utf-8"));
        if (d.token) candidates.push({ src: appAuth, label: "dazi-app", data: d });
      } catch {
      }
    }
    const envToken = process.env.DAZI_AGENT_API_TOKEN ?? process.env.DAZI_TOKEN;
    if (envToken) {
      candidates.push({ src: "ENV:DAZI_AGENT_API_TOKEN", label: "env", data: { token: envToken, serverUrl: process.env.DAZI_BASE_URL } });
    }
    if (!candidates.length) {
      console.log("\u672A\u53D1\u73B0\u53EF\u8FC1\u79FB\u7684\u65E7\u7248\u8BA4\u8BC1\u4FE1\u606F");
      ok({ migrated: false });
      return;
    }
    for (const c of candidates) {
      console.log(`\u53D1\u73B0: [${c.label}] ${c.src}`);
      if (!opts.dryRun) {
        const existing = tryLoadAuth();
        if (existing) {
          console.log("  \u2192 \u5DF2\u5B58\u5728 ~/.dazi/auth.json\uFF0C\u8DF3\u8FC7\uFF08\u907F\u514D\u8986\u76D6\uFF09");
          continue;
        }
        try {
          const user = await apiRequest(
            "/api/auth/me",
            { token: c.data.token, serverUrl: c.data.serverUrl ?? getServerUrl() }
          );
          saveAuth({ token: c.data.token, userId: user.id, username: user.username, email: user.email, serverUrl: c.data.serverUrl ?? getServerUrl(), loginAt: (/* @__PURE__ */ new Date()).toISOString() });
          console.log(`  \u2705 \u8FC1\u79FB\u6210\u529F: ${user.username}`);
        } catch {
          console.log(`  \u26A0\uFE0F  Token \u5DF2\u5931\u6548\uFF0C\u8BF7\u91CD\u65B0\u767B\u5F55: dazi auth login`);
        }
      } else {
        console.log(`  \uFF08dry-run: \u4E0D\u5199\u5165\uFF09`);
      }
    }
    ok({ migrated: !opts.dryRun, candidates: candidates.map((c) => c.label) });
  });
  return cmd;
}

// cli/dazi/src/commands/doctor.ts
var import_os4 = __toESM(require("os"), 1);
function makeDoctorCommand() {
  return new Command("doctor").description("\u68C0\u67E5\u8FD0\u884C\u73AF\u5883").action(async () => {
    const checks = [];
    const nodeVer = process.version;
    const nodeOk = parseInt(nodeVer.slice(1)) >= 18;
    checks.push({ name: "Node.js \u7248\u672C", ok: nodeOk, detail: nodeVer });
    const auth = tryLoadAuth();
    checks.push({ name: "\u767B\u5F55\u72B6\u6001", ok: !!auth, detail: auth ? auth.username : "\u672A\u767B\u5F55" });
    let networkOk = false;
    let networkDetail = "";
    try {
      const url = `${getServerUrl()}/health`;
      const res = await fetch(url, { signal: AbortSignal.timeout(5e3) });
      networkOk = res.ok;
      networkDetail = `${res.status} ${res.statusText}`;
    } catch (err2) {
      networkDetail = String(err2);
    }
    checks.push({ name: `\u7F51\u7EDC\u8FDE\u901A (${getServerUrl()})`, ok: networkOk, detail: networkDetail });
    checks.push({ name: "\u64CD\u4F5C\u7CFB\u7EDF", ok: true, detail: `${import_os4.default.type()} ${import_os4.default.release()} (${import_os4.default.arch()})` });
    let allOk = true;
    for (const c of checks) {
      const icon = c.ok ? "\u2705" : "\u274C";
      console.log(`${icon} ${c.name}: ${c.detail}`);
      if (!c.ok) allOk = false;
    }
    ok({ checks, allOk });
    if (!allOk) process.exit(1);
  });
}

// cli/dazi/src/commands/env.ts
var import_os5 = __toESM(require("os"), 1);
function makeEnvCommand() {
  return new Command("env").description("\u663E\u793A\u73AF\u5883\u4FE1\u606F").action(() => {
    const auth = tryLoadAuth();
    const env = {
      version: "3.0.0-alpha.0",
      node: process.version,
      platform: `${import_os5.default.type()} ${import_os5.default.arch()}`,
      serverUrl: getServerUrl(),
      authFile: authFilePath(),
      configFile: configFilePath(),
      cwd: process.cwd(),
      homeDir: import_os5.default.homedir(),
      loggedIn: !!auth,
      username: auth?.username ?? null
    };
    for (const [k, v] of Object.entries(env)) {
      console.log(`${k.padEnd(16)}: ${v}`);
    }
    ok(env);
  });
}

// cli/dazi/src/commands/data.ts
var import_path5 = __toESM(require("path"), 1);
var import_fs4 = __toESM(require("fs"), 1);
function tableListLabel(t) {
  const display = t.display_name?.trim();
  const physical = (t.table_name ?? t.name ?? "").trim();
  return display || physical || t.id;
}
function normalizeTablesForSummary(tables) {
  return tables.map((t) => ({ ...t, name: tableListLabel(t) }));
}
function dsPrefix(spaceId) {
  return `/api/dataspaces/${spaceId}`;
}
var pipelineDsPrefix = (connectionId) => `/api/data-pipelines/v1/datasources/${encodeURIComponent(connectionId)}`;
function flattenSchemaObjects(groups) {
  const tables = [];
  const seen = /* @__PURE__ */ new Set();
  for (const g of groups) {
    const tableType = g.kind === "view" ? "VIEW" : "TABLE";
    for (const it of g.items ?? []) {
      const name = it.name?.trim();
      if (!name || seen.has(name)) continue;
      seen.add(name);
      tables.push({ name, table_type: tableType });
    }
  }
  return tables;
}
function quoteTableIdent(dbType, tableName) {
  const t = (dbType ?? "").toLowerCase();
  const parts = tableName.split(".");
  if (t === "mysql" || t === "clickhouse") {
    return parts.map((p) => `\`${p.replace(/`/g, "``")}\``).join(".");
  }
  return parts.map((p) => `"${p.replace(/"/g, '""')}"`).join(".");
}
async function loadConnectionType(connectionId) {
  const sources = await apiRequest("/api/connections");
  const hit = sources.find((s) => s.id === connectionId);
  return hit?.db_type ?? hit?.type;
}
async function loadConnectionTables(connectionId, cap) {
  try {
    const resp = await apiRequest(
      `${pipelineDsPrefix(connectionId)}/schema-objects?limit=${cap}`
    );
    const tables = flattenSchemaObjects(resp.groups ?? []);
    if (tables.length) return tables;
  } catch {
  }
  const legacy = await apiRequest(
    `/api/connections/${encodeURIComponent(connectionId)}/tables`
  );
  return (legacy.tables ?? []).slice(0, cap).map((t) => {
    const physical = t.table_name?.trim();
    const schema = t.schema_name?.trim();
    const name = schema && physical && !physical.includes(".") ? `${schema}.${physical}` : physical ?? "";
    return {
      name,
      table_type: t.table_type,
      schema_name: schema
    };
  }).filter((t) => t.name);
}
function printTable(rows) {
  if (!rows.length) return;
  const widths = rows[0].map((_, ci) => Math.max(...rows.map((r) => (r[ci] ?? "").length)));
  for (const row of rows) {
    console.log(row.map((c, i) => c.padEnd(widths[i])).join("  "));
  }
}
function makeSpaceSubCmd() {
  const cmd = new Command("space").description("\u6570\u636E\u7A7A\u95F4\u7BA1\u7406");
  cmd.command("list").description("\u5217\u51FA\u6240\u6709\u6570\u636E\u7A7A\u95F4").option("--json", "\u8F93\u51FA JSON").action(async (opts) => {
    try {
      const spaces = await apiRequest("/api/dataspaces/");
      if (opts.json) {
        console.log(JSON.stringify(spaces, null, 2));
        ok({ spaces });
        return;
      }
      if (!spaces.length) {
        console.log("\uFF08\u6682\u65E0\u6570\u636E\u7A7A\u95F4\uFF09");
        ok({ spaces: [] });
        return;
      }
      printTable([
        ["ID", "NAME", "TABLES", "STATUS"],
        ...spaces.map((s) => [s.id, s.name, String(s.table_count ?? "\u2014"), s.status ?? "active"])
      ]);
      ok({ spaces });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("create <name>").description("\u65B0\u5EFA\u6570\u636E\u7A7A\u95F4").option("--desc <description>", "\u63CF\u8FF0").action(async (name, opts) => {
    try {
      const space = await apiRequest("/api/dataspaces/", {
        method: "POST",
        body: { name, description: opts.desc }
      });
      console.log(`\u2705 \u521B\u5EFA\u6210\u529F: ${space.id}  ${space.name}`);
      ok({ space });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("refresh <spaceId>").description("\u89E6\u53D1\u7A7A\u95F4\u5143\u6570\u636E\u540C\u6B65").action(async (spaceId) => {
    try {
      await apiRequest(`/api/dataspaces/${spaceId}/sync`, { method: "POST" });
      console.log(`\u2705 \u5DF2\u89E6\u53D1\u540C\u6B65: ${spaceId}`);
      ok({ spaceId, synced: true });
    } catch (err2) {
      handleError(err2);
    }
  });
  return cmd;
}
function makeTableSubCmd() {
  const cmd = new Command("table").description("\u6570\u636E\u8868\u7BA1\u7406");
  cmd.command("list").description("\u5217\u51FA\u6570\u636E\u8868").requiredOption("--space <spaceId>", "\u7A7A\u95F4 ID").option("--json", "\u8F93\u51FA JSON").action(async (opts) => {
    try {
      const tables = await apiRequest(`${dsPrefix(opts.space)}/tables`);
      const normalized = normalizeTablesForSummary(tables);
      if (opts.json) {
        console.log(JSON.stringify(tables, null, 2));
        ok({ tables: normalized });
        return;
      }
      if (!tables.length) {
        console.log("\uFF08\u6682\u65E0\u6570\u636E\u8868\uFF09");
        ok({ tables: [] });
        return;
      }
      printTable([
        ["ID", "NAME", "TYPE"],
        ...tables.map((t) => [t.id, tableListLabel(t), t.table_type ?? "\u2014"])
      ]);
      ok({ tables: normalized });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("schema <tableId>").description("\u67E5\u770B\u6570\u636E\u8868\u5217\u7ED3\u6784").requiredOption("--space <spaceId>", "\u7A7A\u95F4 ID").option("--json", "\u8F93\u51FA JSON").action(async (tableId, opts) => {
    try {
      const table = await apiRequest(`${dsPrefix(opts.space)}/tables/${tableId}`);
      const cols = table.columns ?? [];
      if (opts.json) {
        console.log(JSON.stringify(cols, null, 2));
        ok({ columns: cols });
        return;
      }
      if (!cols.length) {
        console.log("\uFF08\u6682\u65E0\u5217\u4FE1\u606F\uFF09");
        ok({ columns: [] });
        return;
      }
      printTable([
        ["COLUMN", "TYPE", "PK", "DESCRIPTION"],
        ...cols.map((c) => [
          c.column_name ?? c.name ?? "",
          c.physical_type ?? c.type ?? "\u2014",
          c.is_primary_key ? "PK" : "",
          c.display_name ?? c.description ?? ""
        ])
      ]);
      ok({ columns: cols });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("sample <tableId>").description("\u9884\u89C8\u6570\u636E\u8868\u524D N \u884C").requiredOption("--space <spaceId>", "\u7A7A\u95F4 ID").option("--limit <n>", "\u884C\u6570", "20").option("--json", "\u8F93\u51FA JSON").action(async (tableId, opts) => {
    try {
      const result = await apiRequest(
        `${dsPrefix(opts.space)}/tables/${tableId}/data?page_size=${opts.limit}`
      );
      const rows = Array.isArray(result.data) ? result.data : [];
      if (opts.json) {
        console.log(JSON.stringify(rows, null, 2));
        ok({ rows });
        return;
      }
      if (!rows.length) {
        console.log("\uFF08\u6682\u65E0\u6570\u636E\uFF09");
        ok({ rows: [] });
        return;
      }
      const colNames = Object.keys(rows[0]);
      printTable([
        colNames,
        ...rows.map((r) => colNames.map((c) => String(r[c] ?? "")))
      ]);
      ok({ rows, count: rows.length });
    } catch (err2) {
      handleError(err2);
    }
  });
  return cmd;
}
function makeSourceSubCmd() {
  const cmd = new Command("source").description("\u6570\u636E\u8FDE\u63A5\u7BA1\u7406");
  cmd.command("list").description("\u5217\u51FA\u6570\u636E\u8FDE\u63A5").option("--json", "\u8F93\u51FA JSON").action(async (opts) => {
    try {
      const sources = await apiRequest("/api/connections");
      if (opts.json) {
        console.log(JSON.stringify(sources, null, 2));
        ok({ sources });
        return;
      }
      if (!sources.length) {
        console.log("\uFF08\u6682\u65E0\u6570\u636E\u8FDE\u63A5\uFF09");
        ok({ sources: [] });
        return;
      }
      printTable([
        ["ID", "NAME", "TYPE", "STATUS"],
        ...sources.map((s) => [s.id, s.name, s.db_type ?? s.type ?? "\u2014", s.status ?? "\u2014"])
      ]);
      ok({ sources });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("tables <connectionId>").description("\u5217\u51FA\u6570\u636E\u8FDE\u63A5\u4E2D\u7684\u8868/\u89C6\u56FE").option("--limit <n>", "\u6700\u591A\u8FD4\u56DE\u6570\u91CF", "500").option("--json", "\u8F93\u51FA JSON").action(async (connectionId, opts) => {
    try {
      const cap = Math.min(Math.max(parseInt(opts.limit, 10) || 500, 1), 2e3);
      const tables = await loadConnectionTables(connectionId, cap);
      const normalized = tables.map((t) => ({
        ...t,
        id: t.name,
        table_name: t.name,
        name: t.name
      }));
      if (opts.json) {
        console.log(JSON.stringify(normalized, null, 2));
        ok({ tables: normalized });
        return;
      }
      if (!tables.length) {
        console.log("\uFF08\u6682\u65E0\u6570\u636E\u8868\uFF09");
        ok({ tables: [] });
        return;
      }
      printTable([
        ["NAME", "TYPE"],
        ...tables.map((t) => [t.name, t.table_type ?? "\u2014"])
      ]);
      ok({ tables: normalized });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("schema <connectionId> <tableName>").description("\u67E5\u770B\u6570\u636E\u8FDE\u63A5\u4E2D\u8868\u7684\u5217\u7ED3\u6784").option("--json", "\u8F93\u51FA JSON").action(async (connectionId, tableName, opts) => {
    try {
      const resp = await apiRequest(
        `${pipelineDsPrefix(connectionId)}/tables/${encodeURIComponent(tableName)}/structure`
      );
      const cols = (resp.columns ?? []).map((c) => ({
        column_name: c.name,
        name: c.name,
        physical_type: c.type,
        type: c.type,
        nullable: c.nullable !== false
      }));
      if (opts.json) {
        console.log(JSON.stringify(cols, null, 2));
        ok({ columns: cols });
        return;
      }
      if (!cols.length) {
        console.log("\uFF08\u6682\u65E0\u5217\u4FE1\u606F\uFF09");
        ok({ columns: [] });
        return;
      }
      printTable([
        ["COLUMN", "TYPE", "NULLABLE"],
        ...cols.map((c) => [c.column_name ?? "", c.physical_type ?? "\u2014", c.nullable ? "YES" : "NO"])
      ]);
      ok({ columns: cols });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("sample <connectionId> <tableName>").description("\u9884\u89C8\u6570\u636E\u8FDE\u63A5\u4E2D\u8868\u7684\u524D N \u884C").option("--limit <n>", "\u884C\u6570", "10").option("--json", "\u8F93\u51FA JSON").action(async (connectionId, tableName, opts) => {
    try {
      const limit = Math.max(parseInt(opts.limit, 10) || 10, 1);
      const dbType = await loadConnectionType(connectionId);
      const quoted = quoteTableIdent(dbType, tableName);
      const sql = `SELECT * FROM ${quoted} LIMIT ${limit}`;
      const resp = await apiRequest(
        "/api/data-pipelines/v1/datasources/query",
        { method: "POST", body: { connection_id: connectionId, sql } }
      );
      const colNames = resp.columns ?? [];
      const rows = (resp.rows ?? []).map((row) => {
        const obj = {};
        colNames.forEach((col, i) => {
          obj[col] = row[i];
        });
        return obj;
      });
      if (opts.json) {
        console.log(JSON.stringify(rows, null, 2));
        ok({ rows });
        return;
      }
      if (!rows.length) {
        console.log("\uFF08\u6682\u65E0\u6570\u636E\uFF09");
        ok({ rows: [] });
        return;
      }
      printTable([
        colNames,
        ...rows.map((r) => colNames.map((c) => String(r[c] ?? "")))
      ]);
      ok({ rows, count: rows.length });
    } catch (err2) {
      handleError(err2);
    }
  });
  return cmd;
}
function makeFileSubCmd() {
  const cmd = new Command("file").description("\u5E73\u53F0\u6587\u4EF6\u7BA1\u7406");
  cmd.command("list").description("\u5217\u51FA\u7A7A\u95F4\u539F\u751F\u811A\u672C\uFF08\u6587\u4EF6\uFF09").requiredOption("--space <spaceId>", "\u7A7A\u95F4 ID").option("--json", "\u8F93\u51FA JSON").action(async (opts) => {
    try {
      const resp = await apiRequest(`${dsPrefix(opts.space)}/native-scripts`);
      const files = resp.scripts ?? [];
      if (opts.json) {
        console.log(JSON.stringify(resp, null, 2));
        ok({ files });
        return;
      }
      if (!files.length) {
        console.log("\uFF08\u6682\u65E0\u539F\u751F\u811A\u672C\uFF09");
        ok({ files: [] });
        return;
      }
      printTable([
        ["NAME", "TYPE"],
        ...files.map((f) => [f.name ?? f.path ?? "", f.type ?? "\u2014"])
      ]);
      ok({ files });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("upload <localFile>").description("\u4E0A\u4F20\u672C\u5730\u6587\u4EF6\u5230\u5E73\u53F0").requiredOption("--space <spaceId>", "\u7A7A\u95F4 ID").option("--dest <destPath>", "\u76EE\u6807\u8DEF\u5F84", "/").action(async (localFile, opts) => {
    try {
      if (!import_fs4.default.existsSync(localFile)) {
        console.error(`\u6587\u4EF6\u4E0D\u5B58\u5728: ${localFile}`);
        process.exit(1);
      }
      const auth = loadAuth();
      const buf = import_fs4.default.readFileSync(localFile);
      const formData = new FormData();
      formData.append("file", new Blob([buf]), import_path5.default.basename(localFile));
      formData.append("destDir", opts.dest);
      formData.append("spaceId", opts.space);
      const url = `${auth.serverUrl.replace(/\/$/, "")}/api/dataspaces/${opts.space}/native-scripts/upload`;
      const res = await fetch(url, {
        method: "POST",
        headers: { Authorization: `Bearer ${auth.token}` },
        body: formData
      });
      if (!res.ok) {
        throw new Error(`\u4E0A\u4F20\u5931\u8D25: ${res.status} ${await res.text()}`);
      }
      const result = await res.json();
      console.log(`\u2705 \u4E0A\u4F20\u6210\u529F: ${result.path}`);
      ok({ path: result.path });
    } catch (err2) {
      handleError(err2);
    }
  });
  return cmd;
}
function makeDataCommand() {
  const cmd = new Command("data").description("\u6570\u636E\u8D44\u6E90\uFF08\u7A7A\u95F4/\u8868/\u6E90/\u6587\u4EF6\uFF09");
  cmd.addCommand(makeSpaceSubCmd());
  cmd.addCommand(makeTableSubCmd());
  cmd.addCommand(makeSourceSubCmd());
  cmd.addCommand(makeFileSubCmd());
  return cmd;
}

// cli/dazi/src/commands/docs.ts
var import_path6 = __toESM(require("path"), 1);
var import_fs5 = __toESM(require("fs"), 1);
function resolveBundledDocsDir() {
  const bundledDir = process.env.DAZI_BUNDLED_DIR;
  if (bundledDir) {
    const p = import_path6.default.resolve(bundledDir, "..", "docs");
    if (import_fs5.default.existsSync(p)) return p;
  }
  const candidates = [
    import_path6.default.resolve(__dirname, "..", "..", "docs"),
    // dist layout
    import_path6.default.resolve(process.execPath, "..", "docs")
  ];
  return candidates.find((c) => import_fs5.default.existsSync(c)) ?? null;
}
function loadBundledIndex(bundledDir) {
  const indexPath = import_path6.default.join(bundledDir, "index.json");
  if (!import_fs5.default.existsSync(indexPath)) return [];
  try {
    const raw = JSON.parse(import_fs5.default.readFileSync(indexPath, "utf-8"));
    return raw.docs ?? [];
  } catch {
    return [];
  }
}
function loadWorkspaceIndex(ws) {
  const indexPath = import_path6.default.join(ws.docs, "index.json");
  if (!import_fs5.default.existsSync(indexPath)) return [];
  try {
    const raw = JSON.parse(import_fs5.default.readFileSync(indexPath, "utf-8"));
    return raw.docs ?? [];
  } catch {
    return [];
  }
}
function makeDocsCommand() {
  const cmd = new Command("docs").description("\u6587\u6863\u7BA1\u7406");
  cmd.command("list").description("\u5217\u51FA\u6240\u6709\u6587\u6863\uFF08\u5185\u7F6E + \u5DE5\u4F5C\u533A\uFF09").option("--category <cat>", "\u8FC7\u6EE4\u5206\u7C7B\uFF08guides/auth/onto/flow/app/data\uFF09").option("--json", "\u8F93\u51FA JSON").action((opts) => {
    try {
      const bundledDir = resolveBundledDocsDir();
      const bundled = bundledDir ? loadBundledIndex(bundledDir) : [];
      const ws = resolveWorkspace();
      const workspace = loadWorkspaceIndex(ws);
      const map = /* @__PURE__ */ new Map();
      bundled.forEach((d) => map.set(d.id, { ...d, source: "bundled" }));
      workspace.forEach((d) => map.set(d.id, { ...d, source: "workspace" }));
      let docs = [...map.values()];
      if (opts.category) docs = docs.filter((d) => d.category === opts.category);
      if (opts.json) {
        console.log(JSON.stringify(docs, null, 2));
        ok({ docs });
        return;
      }
      if (!docs.length) {
        console.log("\uFF08\u6682\u65E0\u6587\u6863\uFF09");
        ok({ docs: [] });
        return;
      }
      const categories = [...new Set(docs.map((d) => d.category))];
      for (const cat of categories) {
        console.log(`
[${cat}]`);
        for (const d of docs.filter((x) => x.category === cat)) {
          console.log(`  ${d.id.padEnd(36)} ${d.title}`);
        }
      }
      ok({ docs });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("open <topicId>").description("\u663E\u793A\u6587\u6863\u5185\u5BB9").action((topicId) => {
    try {
      const ws = resolveWorkspace();
      const bundledDir = resolveBundledDocsDir();
      let content = null;
      let source = "";
      const wsIndex = loadWorkspaceIndex(ws);
      const wsEntry = wsIndex.find((d) => d.id === topicId);
      if (wsEntry) {
        const p = import_path6.default.join(ws.docs, wsEntry.file);
        if (import_fs5.default.existsSync(p)) {
          content = import_fs5.default.readFileSync(p, "utf-8");
          source = "workspace";
        }
      }
      if (!content && bundledDir) {
        const bIndex = loadBundledIndex(bundledDir);
        const bEntry = bIndex.find((d) => d.id === topicId);
        if (bEntry) {
          const p = import_path6.default.join(bundledDir, bEntry.file);
          if (import_fs5.default.existsSync(p)) {
            content = import_fs5.default.readFileSync(p, "utf-8");
            source = "bundled";
          }
        }
      }
      if (!content) {
        console.error(`\u6587\u6863\u672A\u627E\u5230: ${topicId}`);
        process.exit(1);
      }
      console.log(`\u2500\u2500 ${topicId} [${source}] \u2500\u2500
`);
      console.log(content);
      ok({ id: topicId, source });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("sync").description("\u5C06\u5185\u7F6E\u6587\u6863\u540C\u6B65\u5230\u5DE5\u4F5C\u533A \u8D44\u6E90/docs/").option("--force", "\u8986\u76D6\u5DF2\u6709\u6587\u4EF6").option("--from-platform", "\u4ECE\u5E73\u53F0\u540C\u6B65\u6587\u6863\uFF08\u9700\u767B\u5F55\uFF09").option("--dry-run", "\u4EC5\u9884\u89C8").action(async (opts) => {
    try {
      const ws = resolveWorkspace();
      if (!import_fs5.default.existsSync(ws.docs)) import_fs5.default.mkdirSync(ws.docs, { recursive: true });
      if (opts.fromPlatform) {
        const docs = await apiRequest(
          "/api/v1/docs"
        );
        console.log(`\u4ECE\u5E73\u53F0\u83B7\u53D6 ${docs.docs?.length ?? 0} \u7BC7\u6587\u6863`);
        ok({ synced: docs.docs?.length ?? 0, source: "platform" });
        return;
      }
      const bundledDir = resolveBundledDocsDir();
      if (!bundledDir) {
        console.error("\u627E\u4E0D\u5230\u5185\u7F6E\u6587\u6863\u76EE\u5F55\uFF0CDAZI_BUNDLED_DIR \u672A\u8BBE\u7F6E");
        process.exit(1);
      }
      const index = loadBundledIndex(bundledDir);
      let synced = 0, skipped = 0;
      for (const entry of index) {
        const srcFile = import_path6.default.join(bundledDir, entry.file);
        const dstFile = import_path6.default.join(ws.docs, entry.file);
        if (!import_fs5.default.existsSync(srcFile)) continue;
        if (import_fs5.default.existsSync(dstFile) && !opts.force) {
          skipped++;
          if (opts.dryRun) console.log(`  skip (\u5DF2\u5B58\u5728): ${entry.file}`);
          continue;
        }
        if (!opts.dryRun) {
          const dstDir = import_path6.default.dirname(dstFile);
          if (!import_fs5.default.existsSync(dstDir)) import_fs5.default.mkdirSync(dstDir, { recursive: true });
          import_fs5.default.copyFileSync(srcFile, dstFile);
        }
        console.log(`  ${opts.dryRun ? "[dry-run] " : ""}\u2192 ${entry.file}`);
        synced++;
      }
      if (!opts.dryRun) {
        import_fs5.default.copyFileSync(import_path6.default.join(bundledDir, "index.json"), import_path6.default.join(ws.docs, "index.json"));
      }
      console.log(`${opts.dryRun ? "[dry-run] " : ""}\u540C\u6B65 ${synced} \u7BC7\uFF0C\u8DF3\u8FC7 ${skipped} \u7BC7`);
      ok({ synced, skipped, dryRun: opts.dryRun });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("index").description("\u91CD\u5EFA\u5DE5\u4F5C\u533A docs/index.json").action(() => {
    try {
      const ws = resolveWorkspace();
      if (!import_fs5.default.existsSync(ws.docs)) import_fs5.default.mkdirSync(ws.docs, { recursive: true });
      const files = import_fs5.default.readdirSync(ws.docs, { recursive: true }).filter((f) => typeof f === "string" && f.endsWith(".md")).map((f) => ({ file: f.replace(/\\/g, "/"), id: f.replace(/\\/g, "/").replace(/\.md$/, "") }));
      const indexPath = import_path6.default.join(ws.docs, "index.json");
      import_fs5.default.writeFileSync(indexPath, JSON.stringify({ docs: files, updatedAt: (/* @__PURE__ */ new Date()).toISOString() }, null, 2), "utf-8");
      console.log(`\u2705 docs/index.json \u5DF2\u66F4\u65B0 (${files.length} \u7BC7)`);
      ok({ count: files.length });
    } catch (err2) {
      handleError(err2);
    }
  });
  return cmd;
}

// cli/dazi/src/commands/prompt.ts
var import_path7 = __toESM(require("path"), 1);
var import_fs6 = __toESM(require("fs"), 1);
function resolveBundledPromptsDir() {
  const bundledDir = process.env.DAZI_BUNDLED_DIR;
  if (bundledDir) {
    const p = import_path7.default.resolve(bundledDir, "..", "prompts");
    if (import_fs6.default.existsSync(p)) return p;
  }
  const candidates = [
    import_path7.default.resolve(__dirname, "..", "..", "prompts")
  ];
  return candidates.find((c) => import_fs6.default.existsSync(c)) ?? null;
}
function loadIndex(dir) {
  const indexPath = import_path7.default.join(dir, "index.json");
  if (!import_fs6.default.existsSync(indexPath)) return [];
  try {
    const raw = JSON.parse(import_fs6.default.readFileSync(indexPath, "utf-8"));
    return raw.prompts ?? [];
  } catch {
    return [];
  }
}
function makePromptCommand() {
  const cmd = new Command("prompt").description("\u63D0\u793A\u8BCD\u7BA1\u7406");
  cmd.command("list").description("\u5217\u51FA\u6240\u6709\u63D0\u793A\u8BCD\uFF08\u5185\u7F6E + \u5DE5\u4F5C\u533A\uFF09").option("--category <cat>", "\u8FC7\u6EE4\u5206\u7C7B\uFF08onto/flow/app/data/general\uFF09").option("--json", "\u8F93\u51FA JSON").action((opts) => {
    try {
      const bundledDir = resolveBundledPromptsDir();
      const bundled = bundledDir ? loadIndex(bundledDir) : [];
      const ws = resolveWorkspace();
      const wsPromptDir = ws.prompts;
      const workspace = import_fs6.default.existsSync(wsPromptDir) ? loadIndex(wsPromptDir) : [];
      const map = /* @__PURE__ */ new Map();
      bundled.forEach((p) => map.set(p.id, { ...p, source: "bundled" }));
      workspace.forEach((p) => map.set(p.id, { ...p, source: "workspace" }));
      let prompts = [...map.values()];
      if (opts.category) prompts = prompts.filter((p) => p.category === opts.category);
      if (opts.json) {
        console.log(JSON.stringify(prompts, null, 2));
        ok({ prompts });
        return;
      }
      if (!prompts.length) {
        console.log("\uFF08\u6682\u65E0\u63D0\u793A\u8BCD\uFF09");
        ok({ prompts: [] });
        return;
      }
      const categories = [...new Set(prompts.map((p) => p.category))];
      for (const cat of categories) {
        console.log(`
[${cat}]`);
        for (const p of prompts.filter((x) => x.category === cat)) {
          console.log(`  ${p.id.padEnd(36)} ${p.title}`);
        }
      }
      ok({ prompts });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("show <topicId>").description("\u663E\u793A\u63D0\u793A\u8BCD\u5185\u5BB9").option("--copy", "\u8F93\u51FA\u65F6\u9002\u5408\u590D\u5236\uFF08\u65E0 header\uFF09").action((topicId, opts) => {
    try {
      const ws = resolveWorkspace();
      const bundledDir = resolveBundledPromptsDir();
      let content = null;
      let source = "";
      const wsPromptDir = ws.prompts;
      if (import_fs6.default.existsSync(wsPromptDir)) {
        const wsIndex = loadIndex(wsPromptDir);
        const entry = wsIndex.find((p) => p.id === topicId);
        if (entry) {
          const p = import_path7.default.join(wsPromptDir, entry.file);
          if (import_fs6.default.existsSync(p)) {
            content = import_fs6.default.readFileSync(p, "utf-8");
            source = "workspace";
          }
        }
      }
      if (!content && bundledDir) {
        const bIndex = loadIndex(bundledDir);
        const entry = bIndex.find((p) => p.id === topicId);
        if (entry) {
          const p = import_path7.default.join(bundledDir, entry.file);
          if (import_fs6.default.existsSync(p)) {
            content = import_fs6.default.readFileSync(p, "utf-8");
            source = "bundled";
          }
        }
      }
      if (!content) {
        console.error(`\u63D0\u793A\u8BCD\u672A\u627E\u5230: ${topicId}`);
        process.exit(1);
      }
      if (!opts.copy) console.log(`\u2500\u2500 ${topicId} [${source}] \u2500\u2500
`);
      console.log(content);
      ok({ id: topicId, source });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("sync").description("\u5C06\u5185\u7F6E\u63D0\u793A\u8BCD\u540C\u6B65\u5230\u5DE5\u4F5C\u533A \u8D44\u6E90/prompts/").option("--force", "\u8986\u76D6\u5DF2\u6709\u6587\u4EF6").option("--dry-run", "\u4EC5\u9884\u89C8").action((opts) => {
    try {
      const bundledDir = resolveBundledPromptsDir();
      if (!bundledDir) {
        console.error("\u627E\u4E0D\u5230\u5185\u7F6E\u63D0\u793A\u8BCD\u76EE\u5F55");
        process.exit(1);
      }
      const ws = resolveWorkspace();
      const wsPromptDir = ws.prompts;
      if (!import_fs6.default.existsSync(wsPromptDir)) import_fs6.default.mkdirSync(wsPromptDir, { recursive: true });
      const index = loadIndex(bundledDir);
      let synced = 0, skipped = 0;
      for (const entry of index) {
        const srcFile = import_path7.default.join(bundledDir, entry.file);
        const dstFile = import_path7.default.join(wsPromptDir, entry.file);
        if (!import_fs6.default.existsSync(srcFile)) continue;
        if (import_fs6.default.existsSync(dstFile) && !opts.force) {
          skipped++;
          continue;
        }
        if (!opts.dryRun) {
          const dstDir = import_path7.default.dirname(dstFile);
          if (!import_fs6.default.existsSync(dstDir)) import_fs6.default.mkdirSync(dstDir, { recursive: true });
          import_fs6.default.copyFileSync(srcFile, dstFile);
        }
        console.log(`  ${opts.dryRun ? "[dry-run] " : ""}\u2192 ${entry.file}`);
        synced++;
      }
      if (!opts.dryRun) {
        import_fs6.default.copyFileSync(import_path7.default.join(bundledDir, "index.json"), import_path7.default.join(wsPromptDir, "index.json"));
      }
      console.log(`${opts.dryRun ? "[dry-run] " : ""}\u540C\u6B65 ${synced} \u7BC7\uFF0C\u8DF3\u8FC7 ${skipped} \u7BC7`);
      ok({ synced, skipped });
    } catch (err2) {
      handleError(err2);
    }
  });
  return cmd;
}

// cli/dazi/src/commands/examples.ts
var import_path8 = __toESM(require("path"), 1);
var import_fs7 = __toESM(require("fs"), 1);
function resolveBundledExamplesDir() {
  const bundledDir = process.env.DAZI_BUNDLED_DIR;
  if (bundledDir) {
    const p = import_path8.default.resolve(bundledDir, "..", "examples");
    if (import_fs7.default.existsSync(p)) return p;
  }
  const candidates = [
    import_path8.default.resolve(__dirname, "..", "..", "examples")
  ];
  return candidates.find((c) => import_fs7.default.existsSync(c)) ?? null;
}
function loadIndex2(dir) {
  const indexPath = import_path8.default.join(dir, "index.json");
  if (!import_fs7.default.existsSync(indexPath)) return [];
  try {
    const raw = JSON.parse(import_fs7.default.readFileSync(indexPath, "utf-8"));
    return raw.examples ?? [];
  } catch {
    return [];
  }
}
function resolveExampleFile(topicId, wsExamplesDir, bundledDir) {
  if (import_fs7.default.existsSync(wsExamplesDir)) {
    const wsIndex = loadIndex2(wsExamplesDir);
    const wsEntry = wsIndex.find((e) => e.id === topicId);
    if (wsEntry) {
      const p = import_path8.default.join(wsExamplesDir, wsEntry.file);
      if (import_fs7.default.existsSync(p)) {
        return { content: import_fs7.default.readFileSync(p, "utf-8"), source: "workspace", filePath: p };
      }
    }
  }
  if (bundledDir) {
    const bIndex = loadIndex2(bundledDir);
    const bEntry = bIndex.find((e) => e.id === topicId);
    if (bEntry) {
      const p = import_path8.default.join(bundledDir, bEntry.file);
      if (import_fs7.default.existsSync(p)) {
        return { content: import_fs7.default.readFileSync(p, "utf-8"), source: "bundled", filePath: p };
      }
    }
  }
  return null;
}
function makeExamplesCommand() {
  const cmd = new Command("examples").description("\u793A\u4F8B\u811A\u672C\u7BA1\u7406");
  cmd.command("list").description("\u5217\u51FA\u6240\u6709\u793A\u4F8B\uFF08\u5185\u7F6E + \u5DE5\u4F5C\u533A\uFF09").option("--category <cat>", "\u8FC7\u6EE4\u5206\u7C7B\uFF08onto-setup/onto-function \u7B49\uFF09").option("--json", "\u8F93\u51FA JSON").action((opts) => {
    try {
      const bundledDir = resolveBundledExamplesDir();
      const bundled = bundledDir ? loadIndex2(bundledDir) : [];
      const ws = resolveWorkspace();
      const wsExamplesDir = ws.examples;
      const workspace = import_fs7.default.existsSync(wsExamplesDir) ? loadIndex2(wsExamplesDir) : [];
      const map = /* @__PURE__ */ new Map();
      bundled.forEach((e) => map.set(e.id, { ...e, source: "bundled" }));
      workspace.forEach((e) => map.set(e.id, { ...e, source: "workspace" }));
      let examples = [...map.values()];
      if (opts.category) examples = examples.filter((e) => e.category === opts.category);
      if (opts.json) {
        console.log(JSON.stringify(examples, null, 2));
        ok({ examples });
        return;
      }
      if (!examples.length) {
        console.log("\uFF08\u6682\u65E0\u793A\u4F8B\uFF09");
        ok({ examples: [] });
        return;
      }
      const categories = [...new Set(examples.map((e) => e.category))];
      for (const cat of categories) {
        console.log(`
[${cat}]`);
        for (const e of examples.filter((x) => x.category === cat)) {
          console.log(`  ${e.id.padEnd(40)} ${e.title}`);
        }
      }
      ok({ examples });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("show <topicId>").description("\u663E\u793A\u793A\u4F8B\u811A\u672C\u5185\u5BB9\uFF08stdout\uFF09").action((topicId) => {
    try {
      const ws = resolveWorkspace();
      const bundledDir = resolveBundledExamplesDir();
      const resolved = resolveExampleFile(topicId, ws.examples, bundledDir);
      if (!resolved) {
        console.error(`\u793A\u4F8B\u672A\u627E\u5230: ${topicId}`);
        process.exit(1);
      }
      console.log(`\u2500\u2500 ${topicId} [${resolved.source}] \u2500\u2500`);
      console.log(resolved.filePath);
      console.log("");
      console.log(resolved.content);
      ok({ id: topicId, source: resolved.source, file: resolved.filePath });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("sync").description("\u5C06\u5185\u7F6E\u793A\u4F8B\u540C\u6B65\u5230\u5DE5\u4F5C\u533A \u8D44\u6E90/examples/").option("--force", "\u8986\u76D6\u5DF2\u6709\u6587\u4EF6").option("--dry-run", "\u4EC5\u9884\u89C8").action((opts) => {
    try {
      const bundledDir = resolveBundledExamplesDir();
      if (!bundledDir) {
        console.error("\u627E\u4E0D\u5230\u5185\u7F6E\u793A\u4F8B\u76EE\u5F55");
        process.exit(1);
      }
      const ws = resolveWorkspace();
      const wsExamplesDir = ws.examples;
      if (!import_fs7.default.existsSync(wsExamplesDir)) import_fs7.default.mkdirSync(wsExamplesDir, { recursive: true });
      const index = loadIndex2(bundledDir);
      let synced = 0, skipped = 0;
      for (const entry of index) {
        const srcFile = import_path8.default.join(bundledDir, entry.file);
        const dstFile = import_path8.default.join(wsExamplesDir, entry.file);
        if (!import_fs7.default.existsSync(srcFile)) {
          console.warn(`  \u8DF3\u8FC7\uFF08\u6E90\u6587\u4EF6\u7F3A\u5931\uFF09: ${entry.file}`);
          continue;
        }
        if (import_fs7.default.existsSync(dstFile) && !opts.force) {
          skipped++;
          continue;
        }
        if (!opts.dryRun) {
          const dstDir = import_path8.default.dirname(dstFile);
          if (!import_fs7.default.existsSync(dstDir)) import_fs7.default.mkdirSync(dstDir, { recursive: true });
          import_fs7.default.copyFileSync(srcFile, dstFile);
        }
        console.log(`  ${opts.dryRun ? "[dry-run] " : ""}\u2192 ${entry.file}`);
        synced++;
      }
      if (!opts.dryRun) {
        import_fs7.default.copyFileSync(import_path8.default.join(bundledDir, "index.json"), import_path8.default.join(wsExamplesDir, "index.json"));
      }
      console.log(`${opts.dryRun ? "[dry-run] " : ""}\u540C\u6B65 ${synced} \u4E2A\uFF0C\u8DF3\u8FC7 ${skipped} \u4E2A`);
      ok({ synced, skipped });
    } catch (err2) {
      handleError(err2);
    }
  });
  return cmd;
}

// cli/dazi/src/commands/migrate.ts
var import_os6 = __toESM(require("os"), 1);
var import_path9 = __toESM(require("path"), 1);
var import_fs8 = __toESM(require("fs"), 1);
function buildMigratePlan(wsRoot) {
  const actions = [];
  const ontologyDir = import_path9.default.join(wsRoot, "ontology");
  const ontoDir = import_path9.default.join(wsRoot, "onto");
  if (import_fs8.default.existsSync(ontologyDir) && !import_fs8.default.existsSync(ontoDir)) {
    actions.push({ type: "rename", src: ontologyDir, dest: ontoDir, label: "ontology/ \u2192 onto/" });
  } else if (!import_fs8.default.existsSync(ontoDir)) {
    actions.push({ type: "create", dest: ontoDir, label: "\u65B0\u5EFA onto/" });
  }
  const isDrapRoot = (dir) => import_fs8.default.existsSync(import_path9.default.join(dir, "templates")) && import_fs8.default.existsSync(import_path9.default.join(dir, "sdk"));
  const runtimeAppsDir = import_path9.default.join(wsRoot, "runtime-apps");
  const appsDir = import_path9.default.join(wsRoot, "apps");
  if (import_fs8.default.existsSync(runtimeAppsDir) && isDrapRoot(runtimeAppsDir)) {
  } else if (import_fs8.default.existsSync(runtimeAppsDir) && !import_fs8.default.existsSync(appsDir)) {
    actions.push({ type: "rename", src: runtimeAppsDir, dest: appsDir, label: "runtime-apps/ \u2192 apps/" });
  } else if (!import_fs8.default.existsSync(appsDir) && !import_fs8.default.existsSync(runtimeAppsDir)) {
    actions.push({ type: "create", dest: appsDir, label: "\u65B0\u5EFA apps/" });
  }
  const resourcesDir = import_path9.default.join(wsRoot, "\u8D44\u6E90");
  for (const dir of ["flows", "data", ".dazi"]) {
    const p = import_path9.default.join(wsRoot, dir);
    if (!import_fs8.default.existsSync(p)) {
      actions.push({ type: "create", dest: p, label: `\u65B0\u5EFA ${dir}/` });
    }
  }
  if (!import_fs8.default.existsSync(resourcesDir)) {
    actions.push({ type: "create", dest: resourcesDir, label: "\u65B0\u5EFA \u8D44\u6E90/" });
  }
  for (const sub of ["dataspaces", "datasources", "docs", "prompts"]) {
    const p = import_path9.default.join(resourcesDir, sub);
    if (!import_fs8.default.existsSync(p)) {
      actions.push({ type: "create", dest: p, label: `\u65B0\u5EFA \u8D44\u6E90/${sub}/` });
    }
  }
  const cfgPath = import_path9.default.join(wsRoot, ".dazi", "config.json");
  if (!import_fs8.default.existsSync(cfgPath)) {
    actions.push({ type: "copy-config", dest: cfgPath, label: "\u751F\u6210 .dazi/config.json" });
  }
  return actions;
}
function executeActions(actions, wsRoot, backup) {
  if (backup) {
    const ts = (/* @__PURE__ */ new Date()).toISOString().replace(/[:.]/g, "-");
    const backupDir = import_path9.default.join(wsRoot, ".dazi", "backup", ts);
    import_fs8.default.mkdirSync(backupDir, { recursive: true });
    for (const a of actions.filter((x) => x.type === "rename" && x.src)) {
      const backupPath = import_path9.default.join(backupDir, import_path9.default.basename(a.src));
      copyDirSync(a.src, backupPath);
      console.log(`  \u{1F4E6} \u5907\u4EFD: ${a.src} \u2192 ${backupPath}`);
    }
  }
  for (const action of actions) {
    switch (action.type) {
      case "rename":
        import_fs8.default.renameSync(action.src, action.dest);
        console.log(`  \u2705 \u91CD\u547D\u540D: ${action.label}`);
        break;
      case "create":
        import_fs8.default.mkdirSync(action.dest, { recursive: true });
        console.log(`  \u2705 \u521B\u5EFA: ${action.label}`);
        break;
      case "copy-config":
        import_fs8.default.mkdirSync(import_path9.default.dirname(action.dest), { recursive: true });
        import_fs8.default.writeFileSync(action.dest, JSON.stringify({
          migratedAt: (/* @__PURE__ */ new Date()).toISOString(),
          migratedBy: "dazi migrate workspace"
        }, null, 2));
        console.log(`  \u2705 \u751F\u6210: ${action.label}`);
        break;
    }
  }
}
function copyDirSync(src, dest) {
  if (!import_fs8.default.existsSync(src)) return;
  import_fs8.default.mkdirSync(dest, { recursive: true });
  for (const entry of import_fs8.default.readdirSync(src, { withFileTypes: true })) {
    const s = import_path9.default.join(src, entry.name);
    const d = import_path9.default.join(dest, entry.name);
    if (entry.isDirectory()) copyDirSync(s, d);
    else import_fs8.default.copyFileSync(s, d);
  }
}
function makeMigrateCommand() {
  const cmd = new Command("migrate").description("\u8FC1\u79FB\u65E7\u7248\u914D\u7F6E / \u5DE5\u4F5C\u533A");
  cmd.command("config").description("\u5C06\u65E7\u7248 ~/.dazi-app/auth.json \u2192 ~/.dazi/auth.json").action(() => {
    try {
      const legacyPath = import_path9.default.join(import_os6.default.homedir(), ".dazi-app", "auth.json");
      if (!import_fs8.default.existsSync(legacyPath)) {
        console.log("\u672A\u627E\u5230\u65E7\u7248\u8BA4\u8BC1\u6587\u4EF6\uFF0C\u65E0\u9700\u8FC1\u79FB");
        ok({ migrated: false });
        return;
      }
      const legacy = JSON.parse(import_fs8.default.readFileSync(legacyPath, "utf-8"));
      saveAuth({
        token: legacy.token ?? "",
        userId: legacy.userId ?? "",
        username: legacy.username ?? "",
        serverUrl: legacy.serverUrl ?? "https://api.dazi.tech",
        loginAt: (/* @__PURE__ */ new Date()).toISOString()
      });
      console.log("\u2705 \u65E7\u7248\u8BA4\u8BC1\u6587\u4EF6\u5DF2\u8FC1\u79FB\u81F3 ~/.dazi/auth.json");
      ok({ migrated: true, source: legacyPath });
    } catch (err2) {
      handleError(err2);
    }
  });
  cmd.command("workspace").description("\u5C06\u65E7\u7248\u5DE5\u4F5C\u533A\u76EE\u5F55\u5E03\u5C40\u8FC1\u79FB\u81F3 v3 \u89C4\u8303").argument("[dir]", "\u5DE5\u4F5C\u533A\u76EE\u5F55\uFF08\u9ED8\u8BA4\u5F53\u524D\u76EE\u5F55\uFF09", ".").option("--dry-run", "\u4EC5\u9884\u89C8\u53D8\u66F4\uFF0C\u4E0D\u6267\u884C", false).option("--no-backup", "\u8DF3\u8FC7\u5907\u4EFD\u6B65\u9AA4\uFF08\u5371\u9669\uFF09").action((dir, opts) => {
    try {
      const wsRoot = import_path9.default.resolve(dir);
      console.log(`\u5DE5\u4F5C\u533A: ${wsRoot}`);
      if (!import_fs8.default.existsSync(wsRoot)) {
        console.error(`\u76EE\u5F55\u4E0D\u5B58\u5728: ${wsRoot}`);
        process.exit(1);
      }
      const plan = buildMigratePlan(wsRoot);
      if (!plan.length) {
        console.log("\u2705 \u5DE5\u4F5C\u533A\u5DF2\u7B26\u5408 v3 \u89C4\u8303\uFF0C\u65E0\u9700\u8FC1\u79FB");
        ok({ migrated: false, upToDate: true });
        return;
      }
      console.log(`
\u8FC1\u79FB\u8BA1\u5212\uFF08${plan.length} \u9879\uFF09:`);
      for (const a of plan) {
        const prefix = opts.dryRun ? "[dry-run]" : "[execute]";
        console.log(`  ${prefix} ${a.label}`);
      }
      if (opts.dryRun) {
        console.log("\n\uFF08dry-run \u6A21\u5F0F\uFF1A\u672A\u6267\u884C\u4EFB\u4F55\u64CD\u4F5C\uFF09");
        console.log("\u5982\u8981\u6267\u884C\uFF0C\u8BF7\u53BB\u6389 --dry-run \u53C2\u6570");
        ok({ dryRun: true, plan: plan.map((p) => p.label) });
        return;
      }
      executeActions(plan, wsRoot, opts.backup);
      console.log("\n\u2705 \u5DE5\u4F5C\u533A\u8FC1\u79FB\u5B8C\u6210");
      ok({ migrated: true, actions: plan.map((p) => p.label) });
    } catch (err2) {
      handleError(err2);
    }
  });
  return cmd;
}

// cli/dazi/src/commands/quickstart.ts
function makeQuickstartCommand() {
  return new Command("quickstart").description("\u5FEB\u901F\u5F00\u59CB\u5F15\u5BFC").action(() => {
    console.log(`
\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557
\u2551         \u642D\u5B50 v3  \u5FEB\u901F\u5F00\u59CB                    \u2551
\u255A\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255D

1. \u767B\u5F55\u8D26\u53F7:
   dazi auth login

2. \u521D\u59CB\u5316\u5DE5\u4F5C\u533A:
   mkdir my-project && cd my-project
   dazi workspace init

3. \u63A2\u7D22\u529F\u80FD:
   dazi onto --help
   dazi flow --help
   dazi app  --help

4. \u67E5\u770B\u73AF\u5883:
   dazi doctor
`);
    ok({ shown: true });
  });
}

// cli/dazi/src/commands/mcp.ts
var import_path10 = __toESM(require("path"), 1);
var import_fs9 = __toESM(require("fs"), 1);
var import_child_process = require("child_process");
function resolveBundledCliDir() {
  return process.env.DAZI_BUNDLED_DIR ?? null;
}
function resolveBundledRoot() {
  const cliDir = resolveBundledCliDir();
  if (!cliDir) return null;
  const parent = import_path10.default.resolve(cliDir, "..");
  return import_fs9.default.existsSync(parent) ? parent : null;
}
function resolveCli(name) {
  const dir = resolveBundledCliDir();
  if (!dir) return null;
  const p = import_path10.default.join(dir, `${name}.js`);
  return import_fs9.default.existsSync(p) ? p : null;
}
function callCli(cliName, args) {
  const cliPath = resolveCli(cliName);
  if (!cliPath) return { error: `CLI ${cliName} \u672A\u627E\u5230\uFF0C\u8BF7\u786E\u8BA4 DAZI_BUNDLED_DIR \u5DF2\u8BBE\u7F6E` };
  const result = (0, import_child_process.spawnSync)(process.execPath, [cliPath, ...args], {
    encoding: "utf-8",
    timeout: 3e4,
    env: { ...process.env }
  });
  if (result.error) return { error: result.error.message };
  const stdout = result.stdout ?? "";
  const marker = "__JSON_SUMMARY__";
  const idx = stdout.lastIndexOf(marker);
  if (idx !== -1) {
    try {
      const json2 = JSON.parse(stdout.slice(idx + marker.length));
      if (json2.ok) return json2.data ?? {};
      return { error: json2.error?.message ?? "\u547D\u4EE4\u5931\u8D25" };
    } catch {
    }
  }
  return { output: stdout.trim() || result.stderr?.trim() || "\uFF08\u65E0\u8F93\u51FA\uFF09" };
}
function text(s) {
  return { content: [{ type: "text", text: s }] };
}
function json(v) {
  return text(JSON.stringify(v, null, 2));
}
function err(msg) {
  return text(`\u274C \u9519\u8BEF: ${msg}`);
}
function loadDocs() {
  const root = resolveBundledRoot();
  if (!root) return [];
  const idx = import_path10.default.join(root, "docs", "index.json");
  if (!import_fs9.default.existsSync(idx)) return [];
  try {
    return JSON.parse(import_fs9.default.readFileSync(idx, "utf-8")).docs ?? [];
  } catch {
    return [];
  }
}
function loadPrompts() {
  const root = resolveBundledRoot();
  if (!root) return [];
  const idx = import_path10.default.join(root, "prompts", "index.json");
  if (!import_fs9.default.existsSync(idx)) return [];
  try {
    return JSON.parse(import_fs9.default.readFileSync(idx, "utf-8")).prompts ?? [];
  } catch {
    return [];
  }
}
function readFile(filePath) {
  return import_fs9.default.existsSync(filePath) ? import_fs9.default.readFileSync(filePath, "utf-8") : null;
}
var MCP_TOOLS = [
  // ── 文档 ──────────────────────────────────────────────────────────────
  {
    name: "list_docs",
    description: "\u5217\u51FA\u642D\u5B50\u5185\u7F6E\u6587\u6863\u76EE\u5F55\uFF08\u652F\u6301\u6309\u5206\u7C7B\u8FC7\u6EE4\uFF09",
    inputSchema: {
      type: "object",
      properties: {
        category: {
          type: "string",
          enum: ["guides", "auth", "onto", "flow", "app", "data"],
          description: "\u6587\u6863\u5206\u7C7B"
        }
      }
    }
  },
  {
    name: "get_doc",
    description: "\u83B7\u53D6\u6307\u5B9A\u6587\u6863\u7684\u5B8C\u6574 Markdown \u5185\u5BB9\u3002\u5148\u7528 list_docs \u83B7\u53D6 ID \u5217\u8868\u3002",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string", description: "\u6587\u6863 ID\uFF0C\u5982 guides/quickstart\u3001onto/function-guide" }
      },
      required: ["id"]
    }
  },
  // ── 提示词 ────────────────────────────────────────────────────────────
  {
    name: "list_prompts",
    description: "\u5217\u51FA\u642D\u5B50\u5185\u7F6E\u63D0\u793A\u8BCD\u76EE\u5F55",
    inputSchema: {
      type: "object",
      properties: {
        category: {
          type: "string",
          enum: ["onto", "flow", "app", "data", "general"],
          description: "\u63D0\u793A\u8BCD\u5206\u7C7B"
        }
      }
    }
  },
  {
    name: "get_prompt",
    description: "\u83B7\u53D6\u6307\u5B9A\u63D0\u793A\u8BCD\u7684\u5B8C\u6574\u5185\u5BB9\uFF08\u542B\u53D8\u91CF\u5360\u4F4D\u7B26\uFF09",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string", description: "\u63D0\u793A\u8BCD ID\uFF0C\u5982 onto/function-design" }
      },
      required: ["id"]
    }
  },
  // ── 认证 ──────────────────────────────────────────────────────────────
  {
    name: "auth_whoami",
    description: "\u67E5\u770B\u5F53\u524D\u767B\u5F55\u8D26\u53F7\u548C Token \u72B6\u6001",
    inputSchema: { type: "object", properties: {} }
  },
  // ── 本体（onto） ──────────────────────────────────────────────────────
  {
    name: "onto_list_spaces",
    description: "\u5217\u51FA\u6240\u6709\u672C\u4F53\u7A7A\u95F4\uFF08Space\uFF09",
    inputSchema: { type: "object", properties: {} }
  },
  {
    name: "onto_list_functions",
    description: "\u5217\u51FA\u6307\u5B9A\u7A7A\u95F4\u7684\u672C\u4F53\u51FD\u6570\u5B9A\u4E49",
    inputSchema: {
      type: "object",
      properties: {
        space_id: { type: "string", description: "\u7A7A\u95F4 ID" }
      },
      required: ["space_id"]
    }
  },
  {
    name: "onto_get_function",
    description: "\u67E5\u770B\u672C\u4F53\u51FD\u6570\u8BE6\u60C5\uFF08\u542B\u53C2\u6570\u3001\u5165\u53E3\u70B9\u3001\u7248\u672C\uFF09",
    inputSchema: {
      type: "object",
      properties: {
        space_id: { type: "string" },
        function_id: { type: "string" }
      },
      required: ["space_id", "function_id"]
    }
  },
  {
    name: "onto_run_function",
    description: "\u6267\u884C\u672C\u4F53\u51FD\u6570\uFF0C\u8FD4\u56DE\u8F93\u51FA\u7ED3\u679C",
    inputSchema: {
      type: "object",
      properties: {
        space_id: { type: "string" },
        function_id: { type: "string" },
        params: { type: "object", description: "\u51FD\u6570\u53C2\u6570\uFF08JSON \u5BF9\u8C61\uFF09" }
      },
      required: ["space_id", "function_id"]
    }
  },
  {
    name: "onto_list_actions",
    description: "\u5217\u51FA\u6307\u5B9A\u7A7A\u95F4\u7684\u672C\u4F53\u52A8\u4F5C\uFF08Action\uFF09\u5B9A\u4E49",
    inputSchema: {
      type: "object",
      properties: {
        space_id: { type: "string" }
      },
      required: ["space_id"]
    }
  },
  {
    name: "onto_list_rules",
    description: "\u5217\u51FA\u6307\u5B9A\u7A7A\u95F4\u7684\u89C4\u5219",
    inputSchema: {
      type: "object",
      properties: {
        space_id: { type: "string" },
        rule_set: { type: "string", description: "\u89C4\u5219\u96C6\u540D\u79F0\uFF08\u53EF\u9009\uFF09" }
      },
      required: ["space_id"]
    }
  },
  {
    name: "onto_list_scripts",
    description: "\u5217\u51FA\u6307\u5B9A\u7A7A\u95F4\u7684\u811A\u672C",
    inputSchema: {
      type: "object",
      properties: {
        space_id: { type: "string" },
        script_type: { type: "string", description: "\u811A\u672C\u7C7B\u578B\uFF08\u5982 ontology_function\uFF09" }
      },
      required: ["space_id"]
    }
  },
  {
    name: "onto_space_snapshot",
    description: "\u62C9\u53D6\u672C\u4F53\u7A7A\u95F4\u5FEB\u7167\u5230\u672C\u5730 onto/<spaceId>/snapshot.json",
    inputSchema: {
      type: "object",
      properties: {
        space_id: { type: "string" }
      },
      required: ["space_id"]
    }
  },
  // ── 流程（flow） ──────────────────────────────────────────────────────
  {
    name: "flow_list_flows",
    description: "\u5217\u51FA\u6240\u6709 Flow",
    inputSchema: {
      type: "object",
      properties: {
        space_id: { type: "string", description: "\u6309\u7A7A\u95F4\u8FC7\u6EE4\uFF08\u53EF\u9009\uFF09" },
        status: { type: "string", description: "\u6309\u72B6\u6001\u8FC7\u6EE4\uFF08active/draft/archived\uFF09" }
      }
    }
  },
  {
    name: "flow_get_flow",
    description: "\u67E5\u770B Flow \u8BE6\u60C5",
    inputSchema: {
      type: "object",
      properties: {
        flow_id: { type: "string" }
      },
      required: ["flow_id"]
    }
  },
  {
    name: "flow_list_runs",
    description: "\u5217\u51FA Flow \u7684\u6700\u8FD1\u8FD0\u884C\u8BB0\u5F55",
    inputSchema: {
      type: "object",
      properties: {
        flow_id: { type: "string" },
        limit: { type: "number", description: "\u6700\u591A\u8FD4\u56DE\u6761\u6570\uFF08\u9ED8\u8BA4 10\uFF09" },
        status: { type: "string", description: "\u6309\u72B6\u6001\u8FC7\u6EE4\uFF08running/success/failed\uFF09" }
      },
      required: ["flow_id"]
    }
  },
  {
    name: "flow_start_run",
    description: "\u542F\u52A8 Flow\uFF0C\u8FD4\u56DE Run ID \u548C\u521D\u59CB\u72B6\u6001",
    inputSchema: {
      type: "object",
      properties: {
        flow_id: { type: "string" },
        input: { type: "object", description: "\u8F93\u5165\u53C2\u6570\uFF08JSON \u5BF9\u8C61\uFF09" }
      },
      required: ["flow_id"]
    }
  },
  {
    name: "flow_debug_run",
    description: "\u67E5\u770B Flow \u6700\u8FD1\u4E00\u6B21 Run \u7684\u5B8C\u6574\u8C03\u8BD5\u4FE1\u606F\uFF08\u8282\u70B9\u72B6\u6001\u3001\u9519\u8BEF\u3001\u65E5\u5FD7\u672B\u5C3E\uFF09",
    inputSchema: {
      type: "object",
      properties: {
        flow_id: { type: "string" },
        run_id: { type: "string", description: "\u6307\u5B9A Run ID\uFF08\u53EF\u9009\uFF0C\u9ED8\u8BA4\u6700\u8FD1\u4E00\u6B21\uFF09" }
      },
      required: ["flow_id"]
    }
  },
  {
    name: "flow_list_sources",
    description: "\u5217\u51FA\u6570\u636E\u6E90",
    inputSchema: {
      type: "object",
      properties: {
        space_id: { type: "string", description: "\u6309\u7A7A\u95F4\u8FC7\u6EE4\uFF08\u53EF\u9009\uFF09" }
      }
    }
  },
  {
    name: "flow_source_tables",
    description: "\u5217\u51FA\u6570\u636E\u6E90\u4E2D\u7684\u6240\u6709\u8868",
    inputSchema: {
      type: "object",
      properties: {
        source_id: { type: "string" },
        schema: { type: "string", description: "\u8FC7\u6EE4 schema\uFF08\u53EF\u9009\uFF09" }
      },
      required: ["source_id"]
    }
  },
  {
    name: "flow_table_structure",
    description: "\u67E5\u770B\u6570\u636E\u6E90\u4E2D\u67D0\u5F20\u8868\u7684\u5217\u7ED3\u6784\uFF08\u5B57\u6BB5\u540D\u3001\u7C7B\u578B\u3001\u662F\u5426\u53EF\u7A7A\uFF09",
    inputSchema: {
      type: "object",
      properties: {
        source_id: { type: "string" },
        table_name: { type: "string" },
        schema: { type: "string", description: "schema \u540D\uFF08\u53EF\u9009\uFF09" }
      },
      required: ["source_id", "table_name"]
    }
  },
  {
    name: "flow_snapshot_pull",
    description: "\u62C9\u53D6 Flow \u56FE\u5FEB\u7167\u5230\u672C\u5730 flows/<flowId>/snapshot.json",
    inputSchema: {
      type: "object",
      properties: {
        flow_id: { type: "string" }
      },
      required: ["flow_id"]
    }
  },
  {
    name: "flow_plan_llm_guide",
    description: "\u751F\u6210 Flow \u7684 LLM \u5F15\u5BFC\u6587\u6863\uFF08\u4F9B Cursor \u7406\u89E3 Flow \u7ED3\u6784\u548C\u5F00\u53D1\u610F\u56FE\uFF09",
    inputSchema: {
      type: "object",
      properties: {
        flow_id: { type: "string" }
      },
      required: ["flow_id"]
    }
  },
  // ── 数据 （data） ──────────────────────────────────────────────────────
  {
    name: "data_list_spaces",
    description: "\u5217\u51FA\u6570\u636E\u7A7A\u95F4\uFF08ClickHouse \u6570\u636E\u7A7A\u95F4\uFF09",
    inputSchema: { type: "object", properties: {} }
  },
  {
    name: "data_list_tables",
    description: "\u5217\u51FA\u6570\u636E\u7A7A\u95F4\u4E2D\u7684\u6570\u636E\u8868",
    inputSchema: {
      type: "object",
      properties: {
        space_id: { type: "string" }
      },
      required: ["space_id"]
    }
  },
  {
    name: "data_table_schema",
    description: "\u67E5\u770B\u6570\u636E\u8868\u7684\u5B57\u6BB5\u7ED3\u6784\uFF08\u5217\u540D\u3001\u7C7B\u578B\u3001\u662F\u5426\u53EF\u7A7A\uFF09",
    inputSchema: {
      type: "object",
      properties: {
        space_id: { type: "string" },
        table_id: { type: "string" }
      },
      required: ["space_id", "table_id"]
    }
  },
  {
    name: "data_table_sample",
    description: "\u83B7\u53D6\u6570\u636E\u8868\u7684\u91C7\u6837\u6570\u636E\uFF08\u524D N \u884C\uFF09",
    inputSchema: {
      type: "object",
      properties: {
        space_id: { type: "string" },
        table_id: { type: "string" },
        rows: { type: "number", description: "\u91C7\u6837\u884C\u6570\uFF08\u9ED8\u8BA4 10\uFF0C\u6700\u591A 50\uFF09" }
      },
      required: ["space_id", "table_id"]
    }
  }
];
function handleToolCall(name, args) {
  switch (name) {
    case "list_docs": {
      let docs = loadDocs();
      if (args.category) docs = docs.filter((d) => d.category === args.category);
      return json(docs);
    }
    case "get_doc": {
      const root = resolveBundledRoot();
      if (!root) return err("DAZI_BUNDLED_DIR \u672A\u8BBE\u7F6E");
      const entry = loadDocs().find((d) => d.id === String(args.id));
      if (!entry) return err(`\u6587\u6863\u672A\u627E\u5230: ${args.id}\uFF08\u4F7F\u7528 list_docs \u67E5\u770B\u53EF\u7528\u6587\u6863\uFF09`);
      const content = readFile(import_path10.default.join(root, "docs", entry.file));
      return content ? text(content) : err(`\u6587\u6863\u6587\u4EF6\u4E0D\u5B58\u5728: ${entry.file}`);
    }
    case "list_prompts": {
      let prompts = loadPrompts();
      if (args.category) prompts = prompts.filter((p) => p.category === args.category);
      return json(prompts);
    }
    case "get_prompt": {
      const root = resolveBundledRoot();
      if (!root) return err("DAZI_BUNDLED_DIR \u672A\u8BBE\u7F6E");
      const entry = loadPrompts().find((p) => p.id === String(args.id));
      if (!entry) return err(`\u63D0\u793A\u8BCD\u672A\u627E\u5230: ${args.id}\uFF08\u4F7F\u7528 list_prompts \u67E5\u770B\u53EF\u7528\u63D0\u793A\u8BCD\uFF09`);
      const content = readFile(import_path10.default.join(root, "prompts", entry.file));
      return content ? text(content) : err(`\u63D0\u793A\u8BCD\u6587\u4EF6\u4E0D\u5B58\u5728: ${entry.file}`);
    }
    case "auth_whoami": {
      const data = callCli("dazi", ["auth", "whoami"]);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "onto_list_spaces": {
      const data = callCli("dazi-onto", ["space", "list"]);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "onto_list_functions": {
      const data = callCli("dazi-onto", ["function", "list", "--space", String(args.space_id)]);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "onto_get_function": {
      const data = callCli("dazi-onto", ["function", "get", String(args.function_id), "--space", String(args.space_id)]);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "onto_run_function": {
      const params = args.params ? JSON.stringify(args.params) : "{}";
      const data = callCli("dazi-onto", [
        "function",
        "run",
        String(args.function_id),
        "--space",
        String(args.space_id),
        "--params",
        params
      ]);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "onto_list_actions": {
      const data = callCli("dazi-onto", ["action", "list", "--space", String(args.space_id)]);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "onto_list_rules": {
      const ruleArgs = ["rule", "list", "--space", String(args.space_id)];
      if (args.rule_set) ruleArgs.push("--rule-set", String(args.rule_set));
      const data = callCli("dazi-onto", ruleArgs);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "onto_list_scripts": {
      const scriptArgs = ["script", "list", "--space", String(args.space_id)];
      if (args.script_type) scriptArgs.push("--type", String(args.script_type));
      const data = callCli("dazi-onto", scriptArgs);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "onto_space_snapshot": {
      const data = callCli("dazi-onto", ["space", "snapshot", "--space-id", String(args.space_id)]);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "flow_list_flows": {
      const flowArgs = ["flows", "list"];
      if (args.space_id) flowArgs.push("--space", String(args.space_id));
      if (args.status) flowArgs.push("--status", String(args.status));
      const data = callCli("dazi-flow", flowArgs);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "flow_get_flow": {
      const data = callCli("dazi-flow", ["flows", "get", String(args.flow_id)]);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "flow_list_runs": {
      const runArgs = [
        "run",
        "list",
        String(args.flow_id),
        "--limit",
        String(args.limit ?? 10)
      ];
      if (args.status) runArgs.push("--status", String(args.status));
      const data = callCli("dazi-flow", runArgs);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "flow_start_run": {
      const input = args.input ? JSON.stringify(args.input) : "{}";
      const data = callCli("dazi-flow", ["run", "start", String(args.flow_id), "--input", input]);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "flow_debug_run": {
      const debugArgs = ["run", "debug", String(args.flow_id)];
      if (args.run_id) debugArgs.push("--run", String(args.run_id));
      const data = callCli("dazi-flow", debugArgs);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "flow_list_sources": {
      const srcArgs = ["source", "list"];
      if (args.space_id) srcArgs.push("--space", String(args.space_id));
      const data = callCli("dazi-flow", srcArgs);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "flow_source_tables": {
      const tblArgs = ["source", "tables", String(args.source_id)];
      if (args.schema) tblArgs.push("--schema", String(args.schema));
      const data = callCli("dazi-flow", tblArgs);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "flow_table_structure": {
      const strArgs = ["source", "table-structure", String(args.source_id), String(args.table_name)];
      if (args.schema) strArgs.push("--schema", String(args.schema));
      const data = callCli("dazi-flow", strArgs);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "flow_snapshot_pull": {
      const data = callCli("dazi-flow", ["snapshot", "pull", "--flow", String(args.flow_id)]);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "flow_plan_llm_guide": {
      const data = callCli("dazi-flow", ["plan", "llm-guide", String(args.flow_id)]);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "data_list_spaces": {
      const data = callCli("dazi", ["data", "space", "list"]);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "data_list_tables": {
      const data = callCli("dazi", ["data", "table", "list", "--space", String(args.space_id)]);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "data_table_schema": {
      const data = callCli("dazi", [
        "data",
        "table",
        "schema",
        String(args.table_id),
        "--space",
        String(args.space_id)
      ]);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    case "data_table_sample": {
      const rows = String(Math.min(Number(args.rows ?? 10), 50));
      const data = callCli("dazi", [
        "data",
        "table",
        "sample",
        String(args.table_id),
        "--space",
        String(args.space_id),
        "--rows",
        rows
      ]);
      return "error" in data ? err(String(data.error)) : json(data);
    }
    default:
      return err(`\u672A\u77E5\u5DE5\u5177: ${name}\u3002\u4F7F\u7528 tools/list \u67E5\u770B\u53EF\u7528\u5DE5\u5177\u5217\u8868\u3002`);
  }
}
function dispatch(msg) {
  const { id, method, params } = msg;
  const p = params ?? {};
  switch (method) {
    case "initialize":
      return {
        jsonrpc: "2.0",
        id,
        result: {
          protocolVersion: "2024-11-05",
          capabilities: { tools: {} },
          serverInfo: { name: "dazi", version: "3.0.0" }
        }
      };
    case "initialized":
      return null;
    case "tools/list":
      return { jsonrpc: "2.0", id, result: { tools: MCP_TOOLS } };
    case "tools/call": {
      const toolName = String(p.name ?? "");
      const toolArgs = p.arguments ?? {};
      try {
        const result = handleToolCall(toolName, toolArgs);
        return { jsonrpc: "2.0", id, result };
      } catch (e) {
        return { jsonrpc: "2.0", id, result: err(e instanceof Error ? e.message : String(e)) };
      }
    }
    case "ping":
      return { jsonrpc: "2.0", id, result: {} };
    default:
      return {
        jsonrpc: "2.0",
        id,
        error: { code: -32601, message: `Method not found: ${method}` }
      };
  }
}
function makeMcpCommand() {
  const cmd = new Command("mcp").description("MCP \u670D\u52A1\uFF08\u805A\u5408\uFF1Aonto + flow + data + docs + prompts\uFF09");
  cmd.command("stdio").description("\u4EE5 stdio JSON-RPC \u6A21\u5F0F\u542F\u52A8\u642D\u5B50\u805A\u5408 MCP\uFF08\u4F9B Cursor/Claude \u8C03\u7528\uFF09").action(() => {
    const docs = loadDocs().length;
    const prompts = loadPrompts().length;
    process.stderr.write(`[dazi mcp stdio] \u642D\u5B50\u805A\u5408 MCP \u5DF2\u542F\u52A8 \u2014 ${MCP_TOOLS.length} \u4E2A\u5DE5\u5177
`);
    process.stderr.write(`  \u6587\u6863: ${docs} \u7BC7  \u63D0\u793A\u8BCD: ${prompts} \u7BC7
`);
    process.stderr.write(`  onto: ${MCP_TOOLS.filter((t) => t.name.startsWith("onto_")).length} \u4E2A\u5DE5\u5177
`);
    process.stderr.write(`  flow: ${MCP_TOOLS.filter((t) => t.name.startsWith("flow_")).length} \u4E2A\u5DE5\u5177
`);
    process.stderr.write(`  data: ${MCP_TOOLS.filter((t) => t.name.startsWith("data_")).length} \u4E2A\u5DE5\u5177
`);
    let buffer = "";
    process.stdin.setEncoding("utf-8");
    process.stdin.on("data", (chunk) => {
      buffer += chunk;
      const lines = buffer.split("\n");
      buffer = lines.pop() ?? "";
      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const msg = JSON.parse(line);
          const response = dispatch(msg);
          if (response) process.stdout.write(JSON.stringify(response) + "\n");
        } catch {
        }
      }
    });
    process.stdin.on("end", () => {
      process.stderr.write("[dazi mcp stdio] stdin \u5DF2\u5173\u95ED\uFF0C\u9000\u51FA\n");
      process.exit(0);
    });
    ok({ serving: true, tools: MCP_TOOLS.length, docs, prompts });
  });
  cmd.command("tools").description("\u5217\u51FA\u6240\u6709 MCP \u5DE5\u5177").option("--category <cat>", "\u6309\u524D\u7F00\u8FC7\u6EE4\uFF08onto/flow/data/docs\uFF09").action((opts) => {
    let tools = MCP_TOOLS;
    if (opts.category) {
      tools = tools.filter((t) => {
        if (opts.category === "docs") return t.name.startsWith("list_docs") || t.name.startsWith("get_doc") || t.name.startsWith("list_prompts") || t.name.startsWith("get_prompt");
        return t.name.startsWith(`${opts.category}_`);
      });
    }
    console.log(`
\u642D\u5B50 MCP \u5DE5\u5177\uFF08\u5171 ${tools.length} \u4E2A\uFF09
`);
    for (const t of tools) {
      console.log(`  ${t.name.padEnd(32)} ${t.description}`);
    }
    ok({ tools: tools.map((t) => t.name) });
  });
  return cmd;
}

// cli/dazi/src/index.ts
var import_child_process2 = require("child_process");
var import_path11 = __toESM(require("path"), 1);
var import_fs10 = __toESM(require("fs"), 1);
function resolveBundledCli(name) {
  const dir = process.env.DAZI_BUNDLED_DIR;
  if (!dir) return null;
  const p = import_path11.default.join(dir, `${name}.js`);
  return import_fs10.default.existsSync(p) ? p : null;
}
function forwardToCli(cliName, extraArgs) {
  const bundled = resolveBundledCli(cliName);
  let result;
  if (bundled) {
    result = (0, import_child_process2.spawnSync)(process.execPath, [bundled, ...extraArgs], { stdio: "inherit" });
  } else {
    result = (0, import_child_process2.spawnSync)(cliName, extraArgs, { stdio: "inherit", shell: true });
  }
  process.exit(result.status ?? 1);
}
var program2 = new Command();
program2.name("dazi").description("\u642D\u5B50 v3 \u2014 Onto / Flow / App \u7EDF\u4E00 CLI").version("3.0.0", "-v, --version");
program2.addCommand(makeAuthCommand());
program2.addCommand(makeDoctorCommand());
program2.addCommand(makeEnvCommand());
program2.addCommand(makeDataCommand());
program2.addCommand(makeDocsCommand());
program2.addCommand(makePromptCommand());
program2.addCommand(makeExamplesCommand());
program2.addCommand(makeMigrateCommand());
program2.addCommand(makeQuickstartCommand());
program2.addCommand(makeMcpCommand());
program2.command("onto [args...]", { hidden: false }).description("\u672C\u4F53\u7BA1\u7406\uFF08\u8F6C\u53D1\u81F3 dazi-onto\uFF09").allowUnknownOption().action((_args, cmd) => {
  forwardToCli("dazi-onto", process.argv.slice(3));
});
program2.command("flow [args...]", { hidden: false }).description("\u6D41\u7A0B\u7BA1\u7406\uFF08\u8F6C\u53D1\u81F3 dazi-flow\uFF09").allowUnknownOption().action((_args, cmd) => {
  forwardToCli("dazi-flow", process.argv.slice(3));
});
program2.command("app [args...]", { hidden: false }).description("\u5E94\u7528\u7BA1\u7406\uFF08\u8F6C\u53D1\u81F3 dazi-app\uFF09").allowUnknownOption().action((_args, cmd) => {
  forwardToCli("dazi-app", process.argv.slice(3));
});
program2.parseAsync(process.argv).catch((err2) => {
  console.error(err2 instanceof Error ? err2.message : String(err2));
  process.exit(1);
});
