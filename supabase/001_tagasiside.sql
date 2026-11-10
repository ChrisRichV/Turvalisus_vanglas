-- Õppelehe parandusettepanekud ("Teata veast").
-- Avalik leht võib ainult LISADA. Lugeda, muuta ega kustutada anonüümselt ei saa.
-- Ettepanekuid loeb omanik Supabase'i töölaualt (Table editor).

create table if not exists public.oppeleht_tagasiside (
  id        uuid primary key default gen_random_uuid(),
  loodud    timestamptz not null default now(),
  teema     text not null check (char_length(teema) between 1 and 40),
  osa       text check (osa is null or char_length(osa) <= 80),
  tekst     text not null check (char_length(tekst) between 5 and 2000),
  nimi      text check (nimi is null or char_length(nimi) <= 80),
  olek      text not null default 'uus' check (olek in ('uus', 'parandatud', 'tagasi_lykatud'))
);

comment on table public.oppeleht_tagasiside is
  'Turvalisus vanglas õppelehe parandusettepanekud. Anon: ainult INSERT (RLS).';

alter table public.oppeleht_tagasiside enable row level security;

-- Õigused: anon ja authenticated tohivad ainult lisada.
revoke all on table public.oppeleht_tagasiside from anon, authenticated;
grant insert (teema, osa, tekst, nimi) on table public.oppeleht_tagasiside to anon, authenticated;

drop policy if exists "tagasiside_lisamine" on public.oppeleht_tagasiside;
create policy "tagasiside_lisamine"
  on public.oppeleht_tagasiside
  for insert
  to anon, authenticated
  with check (olek = 'uus');

-- SELECT/UPDATE/DELETE poliitikat meelega ei ole → RLS keelab need avalikule võtmele.
