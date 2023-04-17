-- Estruturas

colecoes_estoque (
    id
    colecao
    ativo
)

produtos_estoque (
    id
    id_colecao
    imagem
    produto
    preco
    ativo
)

subprodutos_estoque (
    id
    id_produto
    imagem
    subproduto
    quantidade
    ativo
)

agenda (
    id
    id_produto
    quantidade
    data_entrega
    descricao,
    ativo
)

historico_agenda (
    id
    id_produto
    quantidade
    data_entrega
    descricao
    forma_pagamento
    preco_total
)

#
feiras (
    id
    data_feira
    horario_inicio
    horario_final
    nome_feira
    local_feira
    descricao
    ativo
)

produtos_feira (
    id
    id_feira
    id_produto
    quantidade
    ativo
)

historico_feiras (
    id
    horario_inicio
    horario_final
    nome_feira
    local_feira
    data_feira
    descricao
)

historico_feiras_vendas (
    id
    id_historico_feira
    id_produto
    quantidade
    descricao
    preco
    forma_pagamento
)

feiras_vendas (
    id
    id_feira
    id_produto
    quantidade
    descricao
    preco
    forma_pagamento
    ativo
)

financas_atual (
    id
    nome
    local 
    data 
    forma_pagamento
    preco 
    descricao 
    ativo
)

historico_financas (
    id 
    mes 
    ano
)

historico_financas_compras (
    id 
    id_historico_financas
    nome
    local 
    data 
    forma_pagamento
    preco 
    descricao 
)