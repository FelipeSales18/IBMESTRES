import React, { useEffect, useState } from 'react';

function App() {
  const [produtos, setProdutos] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/produtos/')
      .then(response => response.json())
      .then(data => setProdutos(data));
  }, []);

  return (
    <div>
      <h1>Produtos</h1>
      <ul>
        {produtos.map(produto => (
          <li key={produto.id}>
            <strong>{produto.nome}</strong> - R${produto.preco}
            <p>{produto.descricao}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
