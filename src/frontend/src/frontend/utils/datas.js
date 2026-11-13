import { plural } from './plural.js';

/**
 * Datas em texto para a interface.
 * Aceita Date, "2026-11-12" (só data) ou "2026-11-12T09:30:00" (data e hora).
 * Datas só com dia (AAAA-MM-DD) são lidas no fuso local, para não "voltar um dia".
 */
const MS_POR_DIA = 86_400_000;

export function paraData(valor) {
  if (valor instanceof Date) return valor;
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(valor));
  return m ? new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3])) : new Date(valor);
}

const inicioDoDia = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate());

/** Dias entre hoje e a data: negativo = passado, 0 = hoje, positivo = futuro. */
export function diferencaEmDias(data, agora = new Date()) {
  return Math.round((inicioDoDia(paraData(data)) - inicioDoDia(agora)) / MS_POR_DIA);
}

/** "hoje", "ontem", "amanhã", "há 3 dias", "em 5 dias". */
export function tempoRelativo(data, agora = new Date()) {
  const d = diferencaEmDias(data, agora);
  if (d === 0) return 'hoje';
  if (d === -1) return 'ontem';
  if (d === 1) return 'amanhã';
  return d < 0
    ? `há ${-d} ${plural(-d, 'dia', 'dias')}`
    : `em ${d} ${plural(d, 'dia', 'dias')}`;
}

/** "12/11/2026" */
export function formatarData(data) {
  const d = paraData(data);
  if (Number.isNaN(d.getTime())) return '';
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

/** { dia: "12", mes: "nov" } — usado no selo de data dos lembretes. */
export function partesDoDia(data) {
  const d = paraData(data);
  return {
    dia: String(d.getDate()),
    mes: d.toLocaleDateString('pt-BR', { month: 'short' }).replace('.', ''),
  };
}

/** Texto AAAA-MM-DD de hoje + N dias. Só para os arquivos dados-mock.js. */
export function dataRelativa(dias, base = new Date()) {
  const d = new Date(base.getFullYear(), base.getMonth(), base.getDate() + dias);
  const dois = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${dois(d.getMonth() + 1)}-${dois(d.getDate())}`;
}
