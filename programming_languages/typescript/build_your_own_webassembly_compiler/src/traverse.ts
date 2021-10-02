// Traverse the ast tree in post order
export const traverse: Traverse = (nodes, visitor) => {
  nodes = Array.isArray(nodes) ? nodes : [nodes];
  nodes.forEach((node) => {
    Object.keys(node).forEach((prop: string) => {
      const value = node[prop as keyof ProgramNode];
      const valueAsArray: string[] = Array.isArray(value) ? value : [value];
      valueAsArray.forEach((childNode: any) => {
        if (typeof childNode.type === 'string') {
          traverse(childNode, visitor);
        }
      });
    });
    visitor(node);
  });
};
