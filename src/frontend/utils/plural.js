/** plural(1, 'dia', 'dias') -> 'dia' · plural(3, 'dia', 'dias') -> 'dias' */
export const plural = (n, singular, pluralForma) => (n === 1 ? singular : pluralForma);
