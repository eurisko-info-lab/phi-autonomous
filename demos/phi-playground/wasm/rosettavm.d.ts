/* tslint:disable */
/* eslint-disable */

/**
 * Run a simple calculation (for demos)
 */
export function calculate(expr: string): string;

/**
 * Evaluate RVM assembly code and return the result as a string
 */
export function evaluate(source: string): string;

/**
 * Evaluate a simple expression (for playground)
 */
export function evaluate_expr(source: string): string;

export function init(): void;

/**
 * Parse RVM assembly and return debug info as JSON
 */
export function parse_rvm(source: string): string;

/**
 * Get version info
 */
export function version(): string;

export type InitInput = RequestInfo | URL | Response | BufferSource | WebAssembly.Module;

export interface InitOutput {
  readonly memory: WebAssembly.Memory;
  readonly calculate: (a: number, b: number) => [number, number, number, number];
  readonly evaluate: (a: number, b: number) => [number, number, number, number];
  readonly parse_rvm: (a: number, b: number) => [number, number, number, number];
  readonly version: () => [number, number];
  readonly init: () => void;
  readonly evaluate_expr: (a: number, b: number) => [number, number, number, number];
  readonly __wbindgen_free: (a: number, b: number, c: number) => void;
  readonly __wbindgen_malloc: (a: number, b: number) => number;
  readonly __wbindgen_realloc: (a: number, b: number, c: number, d: number) => number;
  readonly __wbindgen_externrefs: WebAssembly.Table;
  readonly __externref_table_dealloc: (a: number) => void;
  readonly __wbindgen_start: () => void;
}

export type SyncInitInput = BufferSource | WebAssembly.Module;

/**
* Instantiates the given `module`, which can either be bytes or
* a precompiled `WebAssembly.Module`.
*
* @param {{ module: SyncInitInput }} module - Passing `SyncInitInput` directly is deprecated.
*
* @returns {InitOutput}
*/
export function initSync(module: { module: SyncInitInput } | SyncInitInput): InitOutput;

/**
* If `module_or_path` is {RequestInfo} or {URL}, makes a request and
* for everything else, calls `WebAssembly.instantiate` directly.
*
* @param {{ module_or_path: InitInput | Promise<InitInput> }} module_or_path - Passing `InitInput` directly is deprecated.
*
* @returns {Promise<InitOutput>}
*/
export default function __wbg_init (module_or_path?: { module_or_path: InitInput | Promise<InitInput> } | InitInput | Promise<InitInput>): Promise<InitOutput>;
