import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it, vi } from 'vitest'

import { LoginForm } from '@/features/auth/components/LoginForm'

const mutateAsyncMock = vi.fn().mockResolvedValue({ id: '1', email: 'admin@nexus.local', role: 'admin' })

vi.mock('@/features/auth/api/useLogin', () => ({
  useLogin: () => ({ mutateAsync: mutateAsyncMock, isPending: false }),
}))

function renderLoginForm() {
  return render(
    <MemoryRouter>
      <LoginForm />
    </MemoryRouter>,
  )
}

describe('LoginForm', () => {
  it('shows validation errors when submitted empty', async () => {
    const user = userEvent.setup()
    renderLoginForm()

    await user.click(screen.getByRole('button', { name: /sign in/i }))

    expect(await screen.findByText(/email is required/i)).toBeInTheDocument()
    expect(await screen.findByText(/password is required/i)).toBeInTheDocument()
    expect(mutateAsyncMock).not.toHaveBeenCalled()
  })

  it('submits credentials when the form is valid', async () => {
    const user = userEvent.setup()
    renderLoginForm()

    await user.type(screen.getByLabelText(/email/i), 'admin@nexus.local')
    await user.type(screen.getByLabelText(/password/i), 'ChangeMe123!')
    await user.click(screen.getByRole('button', { name: /sign in/i }))

    expect(mutateAsyncMock).toHaveBeenCalledWith({
      email: 'admin@nexus.local',
      password: 'ChangeMe123!',
    })
  })
})
