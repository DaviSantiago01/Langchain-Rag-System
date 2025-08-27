# 📁 Pasta Base - Documentos PDF

Esta pasta é destinada aos seus documentos PDF que serão processados pelo sistema RAG.

## 📋 Instruções

1. **Adicione seus arquivos PDF aqui** - Coloque todos os documentos PDF que você deseja consultar nesta pasta
2. **Formatos suportados** - Apenas arquivos `.pdf` são suportados
3. **Requisitos dos PDFs**:
   - Devem conter texto (não apenas imagens)
   - Preferencialmente em português ou inglês
   - Tamanho recomendado: até 50MB por arquivo

## 🚀 Próximos Passos

Após adicionar seus PDFs:

1. Execute `python criar_db.py` para processar os documentos
2. Execute `python main.py` para começar a fazer perguntas

## 📄 Exemplo de Estrutura

```
base/
├── documento1.pdf
├── documento2.pdf
├── manual_usuario.pdf
└── README.md (este arquivo)
```

## ⚠️ Importante

- **Não commite PDFs sensíveis** - Esta pasta está no `.gitignore` para proteger seus documentos
- **Backup recomendado** - Mantenha cópias dos seus PDFs importantes
- **Reprocessamento** - Sempre que adicionar novos PDFs, execute `criar_db.py` novamente

---

💡 **Dica**: Comece com 2-3 documentos pequenos para testar o sistema antes de adicionar uma grande quantidade de PDFs.